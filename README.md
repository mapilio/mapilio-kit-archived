## Mapilio Kit

Mapilio Tools is a library for processing and uploading images to [Visiosoft](https://www.visiosoft.com.tr/).

<!--ts-->

* [Quickstart](#quickstart)
* [Requirements](#requirements)
* [Installation](#installation)
* [Video Support](#video-support)
* [Usage](#usage)
   - [Authenticate](#authenticate)
   - [Process](#process)
   - [Upload](#upload)
   - [Video Process](#video-process)
* [Download](#download)
* [Advanced Usage](#advanced-usage)
   - [Image Description](#image-description)
<!--te-->	

## Quickstart

Download the latest `mapilio_kit` binaries for your platform
here: https://github.com/mapilio/mapilio_kit/releases/tag/v1.3.6

See [more installation instructions](#installation) below.

## Requirements

### User Authentication

To upload images to Mapilio, an account is required and can be created [here](https://www.mapilio.com/signup). When
using the tools for the first time, user authentication is required. You will be prompted to enter your account
credentials.

### Metadata

To upload images to Mapilio, image `GPS` and `capture time` are minimally required.

## Installation

### Installing via Pip on Ubuntu + 18.04 

Python (3.6 and above) and git are required:

```shell
git clone https://github.com/mapilio/mapilio-kit.git
cd mapilio-kit
chmod +x install.sh
source ./install.sh
```
If you see "Permission Denied" error, try to run the command above with `sudo`

## Video Support

To [process videos](#video-process), you will also need to install `ffmpeg`.

You can download `ffmpeg` from [here](https://ffmpeg.org/download.html). Make sure it is executable and put the
downloaded binaries in your `$PATH`. You can also install `ffmpeg` with your favourite package manager. For example:

On Windows: follower the [instruction](https://www.wikihow.com/Install-FFmpeg-on-Windows)

On macOS, use [Homebrew](https://brew.sh/):

```shell
brew install ffmpeg
```

On Debian/Ubuntu:

```shell
sudo apt install ffmpeg
sudo apt install exiftool
```

## Usage

### User Authentication

To upload images to **Visiosoft**, an account is required and can be created [here](https://www.mapilio.com/). When
using the tools for the first time, user authentication is required. You will be prompted to enter your account
credentials.

### Authenticate

The command `authenticate` will update the user credentials stored in the config file.

#### Examples

Authenticate new user:

```shell
mapilio_kit authenticate
```

Authenticate for user `user_name`. If the user is already authenticated, it will update the credentials in the config:

```shell
mapilio_kit authenticate --user_name "mapilio_user"
```


## Video Support Devices

For now, We have supporting that devices :

| GoPro Hero 9 | GoPro Hero 8 | GoPro Hero 7 | GoPro Max 360 |
|--------------|--------------|--------------|---------------|

## Usage

| Process | Upload | Video Process | Authenticate |
|--------------|--------------|--------------|---------------|

### Process Images

#### Images in Exif (MetaData)

The `process` command **geotags** images in the given directory. It extracts the required and optional metadata from image
EXIF (or the other supported geotag sources), and writes all the metadata (or process errors) in an [image description](#image-description) file, which will be read during [upload](#upload).

**Required MetaData**
| GPS| Captured Time |
|--------------| ---------------|

#### Examples

Process all images in the directory `path/to/images/` (and its sub-directories):

```shell
mapilio_kit process "path/to/images/"
```

#### From .gpx

Interpolate images in the directory `path/to/images/` on the GPX track read from `path/to/gpx_file.gpx`. The images are
required to contain capture time in order to sort the images and interpolate them.

```shell
mapilio_kit process "path/to/images/" \
    --geotag_source "gpx" \
    --geotag_source_path "path/to/gpx_file.gpx"
```

### Upload Images

Images that have been successfully processed can be uploaded with the `upload` command.

#### Examples

Upload all processed images in the directory `path/to/images/` to user `mly_user` for organization `mly_organization_id`
. It is optional to specify `--user_name` if you have only one user [authenticated](#authenticate).

```shell
mapilio_kit upload "path/to/images/" \
    --user_name "mapilio_user" \
    --organization_key "mapilio_organization_id" \
    --project_key "mapilio_project_id"
```

#### 360 panorama image upload command

CSV format must be above;

| Latitude   | Longitude  | CaptureTime             | Altitude | Heading            | SequenceUUID                           | Orientation | DeviceMake | DeviceModel | PhotoUUID                              | filename              |
|------------|------------|-------------------------|----------|--------------------|----------------------------------------|-------------|------------|-------------|----------------------------------------|-----------------------|
| 41.0913264 | 28.8023691 | 2021_10_04_13_26_53_744 | 94.04    | 139.24381082778075 | "9c622173-4561-48f8-a1ed-7ad05e45a8ac" | 1           | GoPro      | HERO9       | "2a0e0105-d733-4d34-bb16-a80b24840a34" | "GH010007_000001.jpg" |



```shell
mapilio_kit image_and_csv_upload "path/to/images" --csv_path "path/to/csv/test.csv"
```

### Mapilio tools to Video Process and Upload

Video process involves two commands:

1. `sample_video`: sample videos into images, and insert capture times to the image EXIF. Capture time is calculated based on the video start time and sampling interval. This is where `ffmpeg` is being used.
2. `process`: process (geotag) the sample images with the specified source

The two commands are usually combined into a single command `video_process`. See the examples below.

#### Examples

## GoPro Hero 9-8-7 Black and 360


**GoPro .mp4 videos**

1. Sample GoPro videos in directory `path/to/videos/` into import path *(must be created before starting*)`path/to/sample_images/` at a sampling rate 1 seconds, i.e. two frames every second, reading geotag data from the GoPro videos in `path/to/videos/`.

```shell
mapilio_kit video_process "path/to/videos/" "path/to/sample_images/" \
    --geotag_source "gopro_videos" \
    --interpolate_directions \
    --video_sample_interval 1
```

2. Checking `path/to/sample_images/` images and `mapilio_description.json` then run under command

```shell
mapilio_kit upload "path/to/sample_images/" --desc_path "mapilio_description.json"
```

**GoPro Max .360 videos**

1. First, the .360 format video is split into 1 second frames. The program to be used for matching since there are gps information in the frames here.
```shell
mapilio_kit video_process "path/to/videos/*.360" "path/to/sample_images360/" \
--geotag_source "gopro_videos" \
--interpolate_directions \
--video_sample_interval 1
```

2. Download 360 video exporter [download](https://www.filehorse.com/download-gopro-max-exporter/) and convert .360 to .mp4 format

```shell
mapilio_kit video_process "path/to/videos/*.mp4" "path/to/sample_imagesMP4/" \
--geotag_source "gopro_videos" \
--interpolate_directions \
--video_sample_interval 1
```

3. And open description file and rename below

`"path/to/sample_images360/IMAGERY_141094.jpg" -> "path/to/sample_imagesMP4/IMAGERY_141094.jpg"`

4. Last step, upload images with description json.

```shell
mapilio_kit upload "path/to/sample_imagesMP4/" --desc_path "description.json"
```

## Download 

If you download your uploaded project to your organization use this command.


```bash
export o_key="281e13Dsdfsd2asd234fddafSXaHGSADFf34"
export p_key="88a1Csa"
mapilio_kit download  "/path/to/download/directory" --organization_key=$o_key --project_key=$p_key --user_name "mapilio@example.com"
```
- After run script select image quality
   - 240
   - 480
   - 1080
- Check the `/path/to/download/directory/MAPILIO/o_key/p_key/[sequence_uuid]`


## Advanced Usage

### Image Description

As the output, the `procss` command generates `mapilio_image_description.json` under the image directory by default.
The file contains an array of objects, each of which records the metadata of one image in the image directory. The
metadata is validated
by [the image description schema](https://github.com/mapilio/mapilio-uploader/tree/master/schema)
. Here is a minimal example:
