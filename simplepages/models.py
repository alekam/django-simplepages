from django.db import models
from django.db.models import fields
from django.utils.html import escape
from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.sites.models import Site


# check for settings or else use defaults
APPEND_SLASH =  getattr(settings, 'SIMPLEPAGES_APPEND_SLASH', True)
PREPEND_SLASH = getattr(settings, 'SIMPLEPAGES_PREPEND_SLASH', True)
IMAGE_DIR = getattr(settings, 'SIMPLEPAGES_IMAGE_DIR', 'images')
PREPOP_PAGE_URL = getattr(settings, 'SIMPLEPAGES_PREPOP_PAGE_URL', True)


class SiteSectionManager(models.Manager):

    def menu_items(self):
        return self.get_query_set().filter(show_in_nav__exact=True)

class SiteSection(models.Model):

    name = models.CharField(max_length=255)
    url = models.CharField(max_length=100, unique=True, blank=False)
    show_in_nav = models.BooleanField(default=True, db_index=True)
    order = models.PositiveIntegerField('Display Order', blank=True, null=True);
    
    class Meta:
        ordering = ('order', 'name')

    def save(self):
        # if enabled, check to ensure the urls start and end with slashes
        if APPEND_SLASH and not self.url.endswith('/'):
            self.url = self.url + '/'
        if PREPEND_SLASH and not self.url.startswith('/'):
            self.url = '/' + self.url

        super(SiteSection, self).save() # call the "real" save() method

    def __unicode__(self):
        return u'%s' % self.name
    
    objects = SiteSectionManager()

class SiteSectionAdmin(admin.ModelAdmin):

    prepopulated_fields = {'url': ('name',)}
    list_display = ('name', 'url', 'order', 'show_in_nav')
    search_fields = ('url', 'name')

admin.site.register(SiteSection, SiteSectionAdmin)


class PageManager(models.Manager):

    def menu_items(self):
        return self.get_query_set().filter(show_in_nav__exact=True).order_by(
                'order', 'nav_title')

class Page(models.Model):

    site_section = models.ForeignKey(SiteSection)
    url = models.CharField('URL', max_length=100, unique=True,
            help_text="Example: '/about-us/contact/'")
    title = models.CharField('Page Title', max_length=200)
    image = models.ImageField(upload_to=IMAGE_DIR,  # media root is automatically prepended
            blank=True)
    content = models.TextField(blank=True)
    show_in_nav = models.BooleanField(default=False, db_index=True,
            help_text='Check this box if this page should be shown in '
            'the primary navigation.')
    nav_title = models.CharField(max_length=150, blank=True,
            help_text='The link text that will show in the navigation menu')
    order = models.PositiveIntegerField(blank=True, null=True,
            help_text="The order this item should appear in the menu, defaults "
            "to alphabetical if order isn't specified");
    html_title = models.CharField(max_length=250, blank=True,
            help_text='This is the browser title')
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)
    template_name = models.CharField('template name', max_length=70, blank=True,
            help_text="Example: 'pages/contact_page.html'. If this isn't "
            "provided, the system will use 'pages/default.html'.")
    registration_required = models.BooleanField('registration required',
            help_text='If this is checked, only logged-in users will be '
            'able to view the page.')

    class Meta:
        ordering = ('order', 'url',)

    def img_src(self):
        return settings.MEDIA_URL + self.image

    def save(self):
        # if enabled, check to ensure the urls start and end with slashes
        if APPEND_SLASH and not self.url.endswith('/'):
            self.url = self.url + '/'
        if PREPEND_SLASH and not self.url.startswith('/'):
            self.url = '/' + self.url
        super(Page, self).save() # call the "real" save() method

    def __unicode__(self):
        return u'%s -- %s' % (self.url, self.title)

    def get_absolute_url(self):
        return self.url

    objects = PageManager()

class PageAdminForm(forms.ModelForm):

    class Meta:
        model = Page

    content = forms.CharField(
                widget=forms.Textarea(attrs={'class': 'simple-html-editor',
                    'rows': 15, 'cols': 70}))

class PageAdmin(admin.ModelAdmin):
    
    form = PageAdminForm
    fieldsets = (
        (None, {'fields': ('site_section', 'url', 'title', 'image', 'content')}),
        ('HTML Header Values', {'fields': ('html_title', 'meta_description', 'meta_keywords', ),'classes': ('collapse',)}),
        ('Nav Menu Setup', {'fields': ('show_in_nav', 'nav_title', 'order'),'classes': ('collapse',)}),
        ('Advanced options', {'classes': ('collapse',), 'fields': ('registration_required', 'template_name')}),
    )
    list_display = ('url', 'title', 'order', 'site_section')
    list_filter = ('site_section',)
    search_fields = ('url', 'title')
    ordering = ('url', 'order')

    class Media:

        js = []
        if PREPOP_PAGE_URL:
            js.append('/simplepages/auto-url-prepend.js')

admin.site.register(Page, PageAdmin)
