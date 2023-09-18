import os
import time
import logging
import flickrapi
import requests
from icecream import ic
from requests.exceptions import RequestException
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('FLICKR_KEY')
api_secret = os.getenv('FLICKR_SECRET')

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
user_id = os.getenv('FLICKR_USERID')

logging.basicConfig(filename='flickr_downloader.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


def create_normalized_directory():
    user_path = input("Enter a directory path: ")
    platform_path = os.path.normpath(user_path)

    if os.name == 'nt':
        platform_path = platform_path.replace('/', '\\')
    else:
        platform_path = platform_path.replace('\\', '/')

    os.makedirs(platform_path, exist_ok=True)
    ic(f"Directory created at {platform_path}")
    return platform_path  # Return the normalized path


# Call the function and store the returned path
download_path = create_normalized_directory()


def download_photo(photo_id):
    try:
        sizes = flickr.photos.getSizes(photo_id=photo_id)['sizes']['size']
        original_size = next(size for size in sizes if size['label'] == 'Original')
        url = original_size['source']

        photo_info = flickr.photos.getInfo(photo_id=photo_id)
        filename = f"{photo_id}_{photo_info['title']}_{photo_info['datetaken']}.jpg"

        # Update this line to use the user-specified download path
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



def get_photos(user_id, page):
    try:
        # Get a list of all photos
        photos = flickr.people.getPhotos(user_id=user_id, page=page)
        return photos
    except Exception as e:
        print(f"Failed to get photos: {e}")
        return None


def get_photo_sizes(photo_id):
    try:
        # Get the URL of the photo in its original size
        sizes = flickr.photos.getSizes(photo_id=photo_id)['sizes']['size']
        return sizes
    except Exception as e:
        print(f"Failed to get photo sizes for photo {photo_id}: {e}")
        return None


def main():
    # Initialize page and pages variables
    page = 1
    pages = 1

    # Initialize request count and start time
    request_count = 0
    start_time = time.time()

    # Initialize a counter for the total number of photos downloaded
    total_downloaded = 0

    # Loop through all pages
    while page <= pages:
        photos = get_photos(user_id, page)
        if photos is None:
            print("No photos found.")
            return

        # Update pages with the total number of pages
        pages = photos['photos']['pages']

        # Download each photo
        for photo in photos['photos']['photo']:
            sizes = get_photo_sizes(photo['id'])
            if sizes is None:
                print(f"Skipping photo {photo['id']} due to error.")
                continue

            download_photo(photo['id'], sizes)

            # Increment request count and total downloaded count
            request_count += 1
            total_downloaded += 1

            # If we've made 3600 requests, sleep until the next hour
            if request_count >= 3600:
                time_to_next_hour = 3600 - (time.time() - start_time)
                print(f"Rate limit reached, sleeping for {time_to_next_hour} seconds...")
                time.sleep(time_to_next_hour)
                # Reset request count and start time
                request_count = 0
                start_time = time.time()
            else:
                # Sleep for a short time to respect rate limits
                time.sleep(2)

            # Print progress report after each photo download
            print(f"Downloaded {total_downloaded} of {photos['photos']['total']} photos.")

        # Go to the next page
        page += 1


if __name__ == "__main__":
    main()

