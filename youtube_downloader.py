import pytube
import os
import pandas as pd


class YoutubeDownloader():
    def __init__(self, download_path = 'downloads', csv_path = 'url_list.csv') -> None:
        self.script_path = os.path.dirname(os.path.abspath(__file__))
        self.download_path = os.path.join(self.script_path, download_path)
        self.csv_path = os.path.join(self.script_path, csv_path)


    def read_csv(self):
        df = pd.read_csv(self.csv_path, header=None)
        return df


    def video_info(self, yt):
        video_dict = {
            'title': yt.title,
            'author': yt.author,
            'length': yt.length,
            'rating': yt.rating,
            'views': yt.views,
            'thumbnail': yt.thumbnail_url,
            'streams': yt.streams,
            'description': yt.description
        }

        return video_dict
    

    def get_yt(self, url):
        yt = pytube.YouTube(url)
        return yt
    

    def download_video(self, yt):
        stream = yt.streams.get_highest_resolution()
        stream.download()


    def download_audio(self, yt, filename):
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(filename=f'{filename}.mp3', output_path=self.download_path)

    
    def download_audio_list(self, url_list):
        for url in url_list:
            yt = self.get_yt(url)
            self.download_audio(yt, self.video_info(yt)['title'])


    def download_audio_csv(self):
        df = self.read_csv()
        for url in df[0]:
            yt = self.get_yt(url)
            self.download_audio(yt, self.video_info(yt)['title'])
            print(f'{self.video_info(yt)["title"]} downloaded')
