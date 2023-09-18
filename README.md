
# Flickr Photo Downloader 📸

## Introduction

Hey there, photo enthusiasts and code lovers! 🌟 Welcome to the Flickr Photo Downloader repository. This Python script is your one-stop solution for downloading all your precious memories stored on Flickr. Whether you're a casual photographer or a professional, this script makes it super easy to back up your photos.

## Features 🌈

- **User-Friendly**: Just run the script, and it will guide you through the process.
- **Customizable**: Choose the directory where you want to save your photos.
- **Robust**: Handles rate limits and other potential errors gracefully.
- **Logging**: Keeps a detailed log of the download process, so you're always in the loop.

## Prerequisites 📝

- Python 3.x
- Flickr API key and secret
- `requests` and `flickrapi` Python packages

## How to Use 🛠️

1. **Clone the Repository**: 
    ```bash
    git clone https://github.com/yourusername/flickr-photo-downloader.git
    ```
   
2. **Install Dependencies**: 
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Environment Variables**: 
    - Create a `.env` file in the root directory.
    - Add your Flickr API key and secret like so:
        ```
        FLICKR_KEY=your_api_key_here
        FLICKR_SECRET=your_api_secret_here
        FLICKR_USERID=your_user_id_here
        ```

4. **Run the Script**: 
    ```bash
    python flickr_downloader.py
    ```

5. **Choose Download Directory**: The script will prompt you to enter a directory path. This is where all your Flickr photos will be downloaded.

6. **Sit Back and Relax**: The script will take care of the rest!

## Contributing 🤝

Feel free to fork this repository and submit pull requests. All contributions are more than welcome!

## License 📜

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Questions? 🤔

Got questions or run into issues? Feel free to reach out to me. Happy downloading! 🎉

---
