from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _

from .forms import FilesFormField, BaseFilesWidget, FilesWidget, ImagesWidget
from topnotchdev.files_widget import controllers
from django.conf import settings


def formfield_defaults(self, default_widget=None, widget=None, form_class=FilesFormField, required=True, **kwargs):
    if not isinstance(widget, BaseFilesWidget):
        widget = default_widget

    defaults = {
        'form_class': FilesFormField,
        'fields': (forms.CharField(required=required), forms.CharField(required=False), forms.CharField(required=False), ),
        'widget': widget,
    }
    defaults.update(kwargs)

    return defaults


def save_all_data(self, instance, data):
    # Save old data to know which images are deleted.
    # We don't know yet if the form will really be saved.
    old_data = getattr(instance, self.name)
    setattr(instance, getattr(settings, 'OLD_VALUE_STR', 'old_%s_value') % self.name, old_data)
    setattr(instance, getattr(settings, 'DELETED_VALUE_STR', 'deleted_%s_value') % self.name, data.deleted_files)
    setattr(instance, getattr(settings, 'MOVED_VALUE_STR', 'moved_%s_valu') % self.name, data.moved_files)


class FilesField(models.TextField):
    description = _("Files")
    attr_class = controllers.FilePaths

    def contribute_to_class(self, cls, name):
        super(FilesField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, controllers.FilesDescriptor(self))

    def save_form_data(self, instance, data):
        print('kkkkkk')
        save_all_data(self, instance, data)
        print(dir(instance))
        super(FilesField, self).save_form_data(instance, data)

    def formfield(self, default_widget=FilesWidget(), **kwargs):
        defaults = formfield_defaults(self, default_widget, **kwargs)
        return super(FilesField, self).formfield(**defaults)


class ImagesField(FilesField):
    description = _("Images")
    attr_class = controllers.ImagePaths

    def formfield(self, default_widget=ImagesWidget(), **kwargs):
        defaults = formfield_defaults(self, default_widget, **kwargs)
        return super(ImagesField, self).formfield(**defaults)
