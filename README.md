## Visiosoft Tools

Visiosoft Tools is a library for processing and uploading images to [Visiosoft](https://www.visiosoft.com.tr/).


## Quickstart

Download the latest `mapilio_tools` binaries for your platform
here: https://github.com/mapilio/mapilio_tools/

Upload imagery:

```shell
mapilio_tools process_and_upload "path/to/images/"
```

## Requirements

### User Authentication

To upload images to Visiosoft, an account is required and can be created [here](https://www.visiosoft.com.tr/). When
using the tools for the first time, user authentication is required. You will be prompted to enter your account
credentials.

## Installation

### Installing via Pip

Python (3.8 and above) and git are required:

```shell
python3 -m pip install --upgrade git+https://github.com/mapilio/mapilio_tools
```

If you see "Permission Denied" error, try to run the command above with `sudo`, or install it in your
local [virtualenv](#development) (recommended).


## Video Support

To [process videos](#video-process), you will also need to install `ffmpeg`.

You can download `ffmpeg` from [here](https://ffmpeg.org/download.html). Make sure it is executable and put the
downloaded binaries in your `$PATH`. You can also install `ffmpeg` with your favourite package manager. For example:

On macOS, use [Homebrew](https://brew.sh/):

```shell
brew install ffmpeg
```

On Debian/Ubuntu:

```shell
sudo apt install ffmpeg
```

## Usage

### Process

The `process` command geotags images in the given directory. It extracts the required and optional metadata from image
EXIF (or the other supported geotag sources), and writes all the metadata (or process errors) in
an [image description](#image-description) file, which will be read during [upload](#upload).

#### Examples

Process all images in the directory `path/to/images/` (and its sub-directories):

```shell
mapilio_tools process "path/to/images/"
```

Interpolate images in the directory `path/to/images/` on the GPX track read from `path/to/gpx_file.gpx`. The images are
required to contain capture time in order to sort the images and interpolate them.

```shell
mapilio_tools process "path/to/images/" \
    --geotag_source "gpx" \
    --geotag_source_path "path/to/gpx_file.gpx"
```

### Upload

Images that have been successfully processed can be uploaded with the `upload` command.

#### Examples

Upload all processed images in the directory `path/to/images/` to user `mly_user` for organization `mly_organization_id`
. It is optional to specify `--user_name` if you have only one user [authenticated](#authenticate).

```shell
mapilio_tools upload "path/to/images/" \
    --user_name "mapilio_user" \
    --organization_key "mapilio_organization_id" \
    --project_key "mapilio_project_id"
```

### VISIOSOFT tools to Video Process and Upload 

Video process involves two commands:

1. `sample_video`: sample videos into images, and insert capture times to the image EXIF. Capture time is calculated
   based on the video start time and sampling interval. This is where `ffmpeg` is being used.
2. `process`: process (geotag) the sample images with the specified source

The two commands are usually combined into a single command `video_process`. See the examples below.

#### Examples

## GoPro Hero 9 Black


**GoPro videos**: Sample GoPro videos in directory `path/to/videos/` into import path `path/to/sample_images/` at a
sampling rate 0.5 seconds, i.e. two frames every second, reading geotag data from the GoPro videos in `path/to/videos/`.

1. Interpolate 1 seconds rate 
```shell
mapilio_tools video_process "path/to/videos/" "path/to/sample_images/" \
    --geotag_source "gopro_videos" \
    --interpolate_directions \
    --video_sample_interval 0.5
```

2. 
```shell
mapilio_tools process "path/to/sample_images/" --desc_path "description.json"
```

3.
```shell
mapilio_tools upload "path/to/sample_images/" --desc_path "description.json"
```

## GoPro Max 360

1. First, the 360 format video is split into 1 second frames. The program to be used for matching since there are gps information in the frames here.
```shell
mapilio_tools video_process "path/to/videos/*.360" "path/to/sample_images360/" \
--geotag_source "gopro_videos" \
--interpolate_directions \
--video_sample_interval 1
```
2. Download 360 video exporter [download](https://www.filehorse.com/download-gopro-max-exporter/) and convert .360 to .mp4 format

```shell
mapilio_tools video_process "path/to/videos/*.mp4" "path/to/sample_imagesMP4/" \
--geotag_source "gopro_videos" \
--interpolate_directions \
--video_sample_interval 1
```

3. Then a description file is created for each frame.
```shell
mapilio_tools process "path/to/sample_images360/" --desc_path "description.json"
```
4. And open description file and change because in path/to/sample_imagesMP4 photos stretched so more quality

`"path/to/sample_images360/IMG_0291.jpg" -> "path/to/sample_imagesMP4/IMG_0291.jpg"`

5. Last step, upload images with description json.

```shell
mapilio_tools upload "path/to/sample_imagesMP4/" --desc_path "description.json"
```




### Authenticate

The command `authenticate` will update the user credentials stored in the config file.

#### Examples

Authenticate new user:

```shell
mapilio_tools authenticate
```

Authenticate for user `mly_user`. If the user is already authenticated, it will update the credentials in the config:

```shell
mapilio_tools authenticate --user_name "mapilio_user"
```

### Aliases

#### `process_and_upload`

`process_and_upload` command will run `process` and `upload` commands consecutively with combined required and optional
arguments. It is equivalent to:

```shell
mapilio_tools process "path/to/images/"
mapilio_tools upload  "path/to/images/"
```

#### `video_process`

`video_process` command will run `sample_video` and `process` commands consecutively with combined required and optional
arguments. It is equivalent to:

```shell
mapilio_tools sample_video "path/to/videos/" "path/to/images/"
mapilio_tools upload "path/to/images/"
```

#### `video_process_and_upload`

`video_process_and_upload` command will run `sample_video` and `process_and_upload` commands consecutively with combined
required and optional arguments. It is equivalent to:

```shell
mapilio_tools sample_video "path/to/videos/" "path/to/videos/mapilio_sampled_video_frames/"
mapilio_tools process_and_upload "path/to/videos/mapilio_sampled_video_frames/"
```

## Advanced Usage

### Image Description

As the output, the `procss` command generates `mapilio_image_description.json` under the image directory by default.
The file contains an array of objects, each of which records the metadata of one image in the image directory. The
metadata is validated
by [the image description schema](https://github.com/mapilio/mapilio_tools/tree/master/schema/image_description_schema.json)
. Here is a minimal example:

```json
[
  {
    "Latitude": 41.5927694,
    "Longitude": 27.1840944,
    "CaptureTime": "2021_02_13_13_24_41_140",
    "filename": "IMG_0291.jpg"
  },
  {
    "error": {
      "type": "mapilioGeoTaggingError",
      "message": "Unable to extract GPS Longitude or GPS Latitude from the image"
    },
    "filename": "IMG_0292.jpg"
  }
]
```

The `upload` command then takes the image description file as the input, [zip images](#zip-images) with the specified
metadata, and then upload. The required `filename` property is used to associate images and metadata objects. Objects
that contain `error` property will be ignored.

#### Examples

Write and read the image description file in another location. This is useful if the image directory is readonly.

```shell
mapilio_tools process "path/to/images/" --desc_path "description.json"
mapilio_tools upload  "path/to/images/" --desc_path "description.json"
# equivalent to
mapilio_tools process_and_upload  "path/to/images/" --desc_path "description.json"
```


### Zip Images

When [uploading](#upload) an image directory, internally the `upload` command will zip sequences in the temporary
directory (`TMPDIR`) and then upload these zip files.

Mapilio Tools provides `zip` command that allows users to specify where to store the zip files, usually somewhere with
faster IO or more free space.

#### Examples:

Zip processed images in `path/to/images/` and write zip files in `path/to/zipped_images/`:

```shell
mapilio_tools zip "path/to/images/" "path/to/zipped_images/"
```

Choose the image description file to write when zipping images:

```shell
mapilio_tools zip "path/to/images/" "path/to/zipped_images/" \
    --desc_path "path/to/image_description.json"
```

Then upload the zip files separately:

```shell
for zipfile in path/to/zipped_images/*.zip; do
    mapilio_tools upload "$zipfile"
    # optionally remove the zipfile after uploaded
    rm "$zipfile"
done
```


#### Examples

```python
import os
from mapilio_tools import uploader

# To obtain your user access token, check https://www.mapilio.com/developer/api-documentation/#authentication
user_item = {
    "user_upload_token": "YOUR_USER_ACCESS_TOKEN",
    "OrganizationKey": 1234,
}
mapilio_uploader = uploader.Uploader(user_item)

descs = [
    {
        "Latitude": 41.5927694,
        "Longitude": 27.1840944,
        "CaptureTime": "2021_02_13_13_24_41_140",
        "filename": "path/to/IMG_0291.jpg",
        "SequenceUUID": "sequence_1",
    },
    {
        "Latitude": 41.5927694,
        "Longitude": 27.1840944,
        "CaptureTime": "2021_02_13_13_24_41_140",
        "filename": "path/to/IMG_0292.jpg",
        "SequenceUUID": "sequence_2",
    },
]

# Upload images as 2 sequences
mapilio_uploader.upload_images(descs)

# Zip images
uploader.zip_images(descs, "path/to/zip_dir")

# Upload zip files
for zip_path in os.listdir("path/to/zip_dir"):
    if zip_path.endswith(".zip"):
      mapilio_uploader.upload_zipfile(zip_path)

```