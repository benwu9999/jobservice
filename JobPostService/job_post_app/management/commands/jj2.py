#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import jinja2
import i18n

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
      [os.path.join(os.path.dirname(__file__), 'view')]),
    extensions=['jinja2.ext.i18n'])

env.install_gettext_translations(i18n)


if __name__ == '__main__':
  template = env.get_template('email_template.html')
  i18n.setLocale("zh_TW")
  d = {'job_posts' : [{'description':'chef', 'location':'home'},
                      {'description': 'waiter', 'location': 'on site'}]}
  print(template.render(d))

  print("\n-----\n")
  #
  # i18n.setLocale("en_US")
  # print(template.render())