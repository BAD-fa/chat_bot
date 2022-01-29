from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class IMedia(ABC):
    location: str
    name: str
    rating: float

    @abstractmethod
    def play_media(self):
        pass


class IMediaPlayer(ABC):
    def __init__(self):
        self.media_list = []

    @abstractmethod
    def set_media_list(self, media_list: List[IMedia]):
        pass

    def get_media_list(self):
        return self.media_list

    def play(self):
        for media in self.media_list:
            media.play_media()

    def play_by_name(self):
        self.media_list = sorted(self.media_list, key=lambda x: x.name)
        self.play()

    def play_by_rating(self):
        self.media_list = sorted(self.media_list, key=lambda x: x.rating)
        self.play()


class IWebMediaPlayer(IMediaPlayer):

    def set_media_list(self, media_list: List[IMedia]):
        for media in media_list:
            if media.location.startswith('https://'):
                self.media_list.append(media)


class ILocalMediaPlayer(IMediaPlayer):

    def set_media_list(self, media_list: List[IMedia]):
        for media in media_list:
            if media.location.startswith('/') or media.location.startswith('c:\\'):
                self.media_list.append(media)


class WebMedia(IMedia):
    def __new__(cls, location, *args, **kwargs):
        if not location.startswith('https://'):
            raise Exception('Wrong media location')
        else:
            return super().__new__(cls)

    def play_media(self):
        print(f"{self.name} in {self.location} is playing")


class LocalMedia(IMedia):
    def __new__(cls, location, *args, **kwargs):
        if location.startswith('/') or location.startswith('c:\\'):
            return super().__new__(cls)
        else:
            raise Exception('Wrong media location')

    def play_media(self):
        print(f"{self.name} in {self.location} is playing")


if __name__ == '__main__':
    wm1 = WebMedia('https://loc1', 'wm1', 1)
    wm2 = WebMedia('https://loc2', 'wm2', 3)
    wm3 = WebMedia('https://loc3', 'wm3', 2)
    wm4 = WebMedia('https://loc4', 'wm4', 4)

    lm1 = LocalMedia('/loc1', 'lm1', 1)
    lm2 = LocalMedia('/loc2', 'lm2', 2)
    lm3 = LocalMedia('c:\\loc3', 'lm3', 3)
    lm4 = LocalMedia('c:\\loc4', 'lm4', 4)
    lm5 = LocalMedia('/loc5', 'lm5', 5)

    ilm = ILocalMediaPlayer()
    iwm = IWebMediaPlayer()

    ilm.set_media_list([wm4, wm3, lm1, lm2, lm3])
    iwm.set_media_list([wm1, wm2, wm3])

    ilm.get_media_list()
    print('ilm by name')
    ilm.play_by_name()
    print('ilm by rate')
    ilm.play_by_rating()

    iwm.get_media_list()
    print('iwm by name')
    iwm.play_by_name()
    print('iwm by rate')
    iwm.play_by_rating()
