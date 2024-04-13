# carousel.py
#
# Copyright 2023 Nokse
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gio

from ..lib import utils

@Gtk.Template(resource_path='/io/github/nokse22/HighTide/ui/widgets/carousel_widget.ui')
class CarouselWidget(Gtk.Box):
    __gtype_name__ = 'CarouselWidget'

    """It is used to display multiple elements side by side with navigation arrows"""

    title_label = Gtk.Template.Child()
    next_button = Gtk.Template.Child()
    prev_button = Gtk.Template.Child()
    carousel = Gtk.Template.Child()
    more_button = Gtk.Template.Child()

    def __init__(self, title=""):
        super().__init__()

        self.n_pages = 0

        self.title_label.set_label(title)

        self.more_item = None

        # self.card_width = 0
        # self.connect("notify::width", self._width_changed)

    def set_more_action(self, item, function):
        self.more_button.set_visible(True)
        self.more_item = item
        self.more_function = function

    def append_card(self, card):
        self.carousel.append(card)
        self.n_pages = self.carousel.get_n_pages()

        if self.n_pages != 2:
            self.next_button.set_sensitive(True)

        # if self.card_width == 0:
        #     self.card_width = card.get_width()

    # def _width_changed(self):
    #     width = self.carousel.get_width()
    #     if width >= 2 * self.card_width:
    #         print("wide")
    #     print("width")

    @Gtk.Template.Callback("on_more_clicked")
    def on_more_clicked(self, *args):
        from ..pages import singleTypePage

        self.more_item

        page = singleTypePage(self, self.more_item, "Favourite Tracks")
        page.load()
        self.navigation_view.push(page)

    @Gtk.Template.Callback("on_next_clicked")
    def carousel_go_next(self, btn):
        pos = self.carousel.get_position()
        if pos + 2 >= self.carousel.get_n_pages():
            if pos + 1 == self.carousel.get_n_pages():
                return
            else:
                next_page = self.carousel.get_nth_page(pos + 1)
        else:
            next_page = self.carousel.get_nth_page(pos + 2)

        if next_page != None:
            self.carousel.scroll_to(next_page, True)

        self.prev_button.set_sensitive(True)

    @Gtk.Template.Callback("on_prev_clicked")
    def carousel_go_prev(self, btn):
        pos = self.carousel.get_position()
        if pos - 2 < 0:
            if pos - 1 < 0:
                return
            else:
                next_page = self.carousel.get_nth_page(0)
        else:
            next_page = self.carousel.get_nth_page(pos - 2)

        self.carousel.scroll_to(next_page, True)

        if pos - 2 <= 0:
            self.prev_button.set_sensitive(False)
