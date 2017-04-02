from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse

import requests
import re
from io import open as iopen


class TVShow(models.Model):
    """
    TV show model:

    """
    title = models.CharField(max_length=100, unique=True)
    display_title = models.CharField(max_length=100, unique=True)
    imdb_url = models.CharField(max_length=1000, unique=True)
    imdb_img_url = models.CharField(max_length=1000, unique=True)

    current_season = models.PositiveIntegerField()
    last_seen_episode = models.PositiveIntegerField()
    is_next_episode_available = models.BooleanField()
    next_episode_date = models.DateField(default=None, null=True)

    update_date = models.DateTimeField(default=None)

    def __str__(self):
        """
        Readable str output.
        """
        return self.display_title

    def add_new(self, title):
        """
        add a new TV show to the database.
        """
        self.title = title.lower() # title must be only lower case
        self.find_imdb_url() # find the IMDB tv show page url
        self.get_imdb_info() # retreive the information from the IMDB page
        self.update_tvshow() # update the TV show object (and save it)

    def find_imdb_url(self):
        """
        find the TV show page on imdb.
        """
        title_search = self.title.replace(' ', '+')
        title_search = title_search.replace("'", "%27")
        imdb_search_link = 'http://www.imdb.com/find?ref_=nv_sr_fn&q=%s&s=tt' % title_search
        imdb_search_result = requests.get(imdb_search_link).text

        # retreive the first result
        imdb_url_regex = '<tr class="findResult odd"> <td class="primary_photo"> <a href="(?P<imdb_tvshow_url>[^<>]+)" ><img src="[^<>]+" /></a> </td> <td class="result_text"> <a href="[^<>]+" >[^<>]+</a> \(\d+\) \(TV Series\) </td> </tr>'

        try:
            result = re.finditer(imdb_url_regex, imdb_search_result).next()
            self.imdb_url = 'http://www.imdb.com' + result.groupdict()['imdb_tvshow_url']
        except StopIteration:
            raise ValueError("Can't find IMDB url of tv show %s" % self.title)

    def get_imdb_info(self):
        """
        Find all the information of a given TV show from IMDB
        """
        imdb_page = requests.get(self.imdb_url).text

        imdb_img_url_regex = '<img alt="[^<>]+ Poster" title="[^<>]+ Poster"\nsrc="(?P<imdb_tvshow_image>[^<>]+)"\nitemprop="image" />'
        imdb_display_title_regex = '<div class="title_wrapper">\n<h1 itemprop="name" class="">(?P<imdb_display_title>[^<>]+)&nbsp;            </h1>'
        imdb_original_title_regex = '<div class="originalTitle">(?P<imdb_original_title>[^<>]+)<span class="description"> \(original title\)</span></div>'
        
        # search for original title first
        # if it doesnt exist read the display title
        try:
            result = re.finditer(imdb_original_title_regex, imdb_page).next()
            self.display_title = result.groupdict()['imdb_original_title']
        except StopIteration:
            try:
                result = re.finditer(imdb_display_title_regex, imdb_page).next()
                self.display_title = result.groupdict()['imdb_display_title']
            except StopIteration:
                raise ValueError("Can't find %s tv show IMDB display title" % self.title)

        # get the imdb image
        try:
            result = re.finditer(imdb_img_url_regex, imdb_page).next()
            imdb_img_url = result.groupdict()['imdb_tvshow_image']
            self.imdb_img_url = imdb_img_url
        except StopIteration:
            raise ValueError("Can't find %s tv show IMDB poster" % self.title)

    def update_tvshow(self):
        """
        update a TV show of the database.
        """
        self.current_season = 1
        self.last_seen_episode = 1
        self.is_next_episode_available = True
        self.update_date = timezone.now()
        self.save()

    def add_season(self):
        """
        Add a season to our TV show
        """
        season = Season()
        season.number = self.seasons.count() + 1
        season.tvshow = self
        season.save()
        self.seasons.add(season)

    def get_absolute_url(self):
        """
        Return the TV show page url
        """
        return reverse('Series:tvshow_page', kwargs={'tvshow_pk':self.pk})


class Season(models.Model):
    """
    Season model:

    """
    tvshow = models.ForeignKey(TVShow, related_name='seasons', on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        """
        Readable str output.
        """
        str_output = self.tvshow.display_title
        str_output += ' Season ' + str(self.number)
        return str_output

    def add_episode(self, name=None):
        """
        Add an episode to the season
        """
        episode = Episode()
        episode.number = self.episodes.count() + 1
        episode.name = name or episode.name
        episode.season = self
        episode.save()
        self.episodes.add(episode)

    def all_seen(self):
        """
        set all episodes to seen
        """
        for episode in self.episodes.all():
            episode.seen = True
            episode.save()

class Episode(models.Model):
    season = models.ForeignKey(Season, related_name='episodes', on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=100, default='unknown', null=True)
    seen = models.BooleanField(default=False)
    available = models.BooleanField(default=False)
    magnet_link = models.TextField()

    def __str__(self):
        """
        Readable str output.
        """
        str_output = self.season.tvshow.display_title
        str_output += ' Season ' + str(self.season.number)
        str_output += ' Episode ' + str(self.number)  
        return str_output

    def get_magnet_link(self):
        pass


def requests_image(file_url, filename):
    """
    Retrieve a image file from a given url and save it at the target location.
    It also returns it's extension.
    """
    suffix_list = ['.jpg', '.gif', '.png', '.tif', '.svg', '.jpeg']
    file_suffix = '.' + file_url.split('.')[-1]
    output_filename = filename + file_suffix
    i = requests.get(file_url)
    if file_suffix in suffix_list and i.status_code == requests.codes.ok:
        with iopen(output_filename, 'wb') as file:
            file.write(i.content)
        return file_suffix
    else:
        return False