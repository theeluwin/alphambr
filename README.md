# AlphaMBR

Alpha-channel invoked Minimum Bounding Rectangle.

![AlphaMBR Example](https://user-images.githubusercontent.com/1303549/76687626-8afad300-661d-11ea-8e6c-af3156dfe42a.png)

## Installation

Just place this `alphambr.py` file into some appropriate location.

## Usage

```python
from alphambr import Alphambr
from skimage.io import imread
from skimage.io import imsave

ambr = Alphambr(
    cut_margin=1,
    add_padding=12,
    alpha_threshold=1,
    max_component_count=2,
    min_component_size=50 * 50
)

image = imread(your_image_path)
mbred = ambr(image)  # it's a functor!
imsave(your_save_path, mbred)
```

## Parameters

* `cut_margin`: cut image margin

* `add_padding`: add paddings for bounding rectangle

* `alpha_threshold`: threshold for alpha channel (1 ~ 255)

* `max_component_count`: max component count, use all if `None`

* `min_component_size`: min component size, use all if `None`

## How it works?

1. Apply connected components algorithm from OpenCV.

2. Remove unnecessary components (by count limit or size limit).

3. Calculate MBR coordinates.

## Example

See `example.py` for examples.

You can use docker for testing.

```bash
$ docker build -t alphambr -f Dockerfile .
$ docker run --rm -it --init -v "${PWD}:/workspace" alphambr python example.py
```
