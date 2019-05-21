import os
import os.path as op
from PIL import Image
from wtforms.widgets import html_params, HTMLString
import ast
from flask_admin import form
from flask_admin._compat import string_types, urljoin
from wtforms.utils import unset_value
from flask_admin.helpers import get_url
from flask_admin.form.upload import ImageUploadField
import datetime

class MultipleImageUploadInput(object):
    empty_template = "<input %(file)s multiple>"

    # display multiple images in edit view of quart-admin
    data_template = ("<div class='image-thumbnail'>"
                     "   %(images)s"
                     "</div>"
                     "<input %(file)s multiple>")

    def __call__(self, field, **kwargs):

        kwargs.setdefault("id", field.id)
        kwargs.setdefault("name", field.name)

        args = {
            "file": html_params(type="file", **kwargs),
        }

        if field.data and isinstance(field.data, string_types):

            attributes = self.get_attributes(field)

            args["images"] = "&emsp;".join(["<img src='{}' /><input type='checkbox' name='{}-delete'>Delete</input>"
                                           .format(src, filename) for src, filename in attributes])

            template = self.data_template

        else:
            template = self.empty_template

        return HTMLString(template % args)

    def get_attributes(self, field):

        for item in ast.literal_eval(field.data):

            filename = item

            # if field.thumbnail_size:
            #     filename = field.thumbnail_size(filename)

            if field.url_relative_path:
                filename = urljoin(field.url_relative_path, filename)

            yield get_url(field.endpoint, filename=filename), item


class MultipleImageUploadField(ImageUploadField):
    widget = MultipleImageUploadInput()

    def process(self, formdata, data=unset_value):

        self.formdata = formdata  # get the formdata to delete images
        return super(MultipleImageUploadField, self).process(formdata, data)

    def process_formdata(self, valuelist):

        self.data = list()

        for value in valuelist:
            if self._is_uploaded_file(value):
                self.data.append(value)

    def populate_obj(self, obj, name):

        field = getattr(obj, name, None)

        if field:

            filenames = ast.literal_eval(field)

            for filename in filenames[:]:
                if filename + "-delete" in self.formdata:
                    print ("delete",filename)
                    self._delete_file(filename)
                    filenames.remove(filename)
        else:
            filenames = list()

        for data in self.data:
            if self._is_uploaded_file(data):
                self.image = Image.open(data)

                filename = self.generate_name(obj, data)
                ext = filename.split(".")[-1]
                main_name = filename.split(".")[0]

                suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
                filename = "_".join([main_name, suffix]) + "." + ext

                filename = self._save_file(data, filename)

                data.filename = filename

                filenames.append(filename)

        setattr(obj, name, str(filenames))

    def _delete_file(self, filename):
        path = self._get_path(filename)
        thumb_path = self._get_path(form.thumbgen_filename(filename))
        print ("delete thumb path :",thumb_path)
        if op.exists(path):
            print ("prepare for delete main file")
            os.remove(path)
        if op.exists(thumb_path):
            print ("prepare for delete thumb file")
            os.remove(thumb_path)
