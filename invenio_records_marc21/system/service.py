# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Marc21 Record Resource."""


from flask_resources import route

from . import config
from .models import Marc21Templates


#
# Records
#
class Marc21TemplateService:
    """Marc21 template resource."""

    config_name = "MARC21_TEMPLATE_CONFIG"
    default_config = config.Marc21TemplateConfig
    template_cls = Marc21Templates

    def __init__(self, config):
        """Constructor for Marc21TemplateService."""
        self.config = config

    def create(self, name, data):
        """Create a template for a new record."""
        return self._create(self.template_cls, name, data)

    def _create(self, template_cls, name, data):
        template = template_cls.create(name=name, data=data)
        return template

    def get_templates(self, names=None, with_deleted=False):
        """Get templates for a new record."""
        return self.template_cls.get_templates(names=names, with_deleted=with_deleted)

    def get_template(self, name):
        """Get a template for a new record."""
        return self.template_cls.get_template(name=name)

    def delete(self, all, force, name):
        """Create a template for a new record."""
        if all:
            return self._deleteall(self.template_cls, force=force)
        return self._delete(self.template_cls, name=name, force=force)

    def _delete(self, template_cls, name, force):
        """Create a template for a new record."""
        return template_cls.delete(name=name, force=force)

    def _deleteall(self, template_cls, force):
        """Create a template for a new record."""
        return template_cls.deleteall(force=force)
