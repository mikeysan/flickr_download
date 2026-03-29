import os
import time
import logging
import flickrapi
import requests
from icecream import ic
from requests.exceptions import RequestException
from dotenv import load_dotenv


def create_normalized_directory():
    user_path = input("Enter a directory path: ")
    platform_path = os.path.normpath(user_path)

    if os.name == 'nt':
        platform_path = platform_path.replace('/', '\\')
    else:
        platform_path = platform_path.replace('\\', '/')

    os.makedirs(platform_path, exist_ok=True)
    ic(f"Directory created at {platform_path}")
    return platform_path


def download_photo(photo_id, flickr, download_path, sizes=None):
    try:
        if sizes is None:
            sizes = flickr.photos.getSizes(photo_id=photo_id)['sizes']['size']

        original_size = next(size for size in sizes if size['label'] == 'Original')
        url = original_size['source']

        photo_info = flickr.photos.getInfo(photo_id=photo_id)

        ext = os.path.splitext(url.split('?')[0])[1] or '.jpg'
        filename = f"{photo_id}_{photo_info['title']}_{photo_info['datetaken']}{ext}"
        filename = os.path.join(download_path, filename)

        if os.path.isfile(filename):
            logging.info(f"Photo {photo_id} already downloaded. Skipping...")
            return

        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        logging.info(f"Downloaded photo {photo_id}")
    except RequestException as e:
        logging.error(f"Failed to download photo {photo_id}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error when downloading photo {photo_id}: {e}")


def get_photos(flickr, user_id, page):
    try:
        photos = flickr.people.getPhotos(user_id=user_id, page=page)
        return photos
    except Exception as e:
        print(f"Failed to get photos: {e}")
        return None


def get_photo_sizes(flickr, photo_id):
    try:
        sizes = flickr.photos.getSizes(photo_id=photo_id)['sizes']['size']
        return sizes
    except Exception as e:
        print(f"Failed to get photo sizes for photo {photo_id}: {e}")
        return None


def main():
    load_dotenv()

    api_key = os.getenv('FLICKR_KEY')
    api_secret = os.getenv('FLICKR_SECRET')
    user_id = os.getenv('FLICKR_USERID')

    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

    logging.basicConfig(
        filename='flickrdl.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
    )

    download_path = create_normalized_directory()

    page = 1
    pages = 1
    request_count = 0
    start_time = time.time()
    total_downloaded = 0

    while page <= pages:
        photos = get_photos(flickr, user_id, page)
        if photos is None:
            print("No photos found.")
            return

        pages = photos['photos']['pages']

        for photo in photos['photos']['photo']:
            sizes = get_photo_sizes(flickr, photo['id'])
            if sizes is None:
                print(f"Skipping photo {photo['id']} due to error.")
                continue

            download_photo(photo['id'], flickr, download_path, sizes)

            request_count += 1
            total_downloaded += 1

            if request_count >= 3600:
                time_to_next_hour = 3600 - (time.time() - start_time)
                print(f"Rate limit reached, sleeping for {time_to_next_hour} seconds...")
                time.sleep(time_to_next_hour)
                request_count = 0
                start_time = time.time()
            else:
                time.sleep(2)

            print(f"Downloaded {total_downloaded} of {photos['photos']['total']} photos.")

        page += 1


if __name__ == "__main__":
    main()
