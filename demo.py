import torch
import torch as t

from model import Siamese, load_model, get_custom_CNN, jit_load, get_parametrized_model
from torchvision.transforms import Resize
from utils import get_shift, plot_samples, plot_displacement
import numpy as np
from scipy import interpolate
from torchvision.io import read_image

device = t.device("cuda") if t.cuda.is_available() else t.device("cpu")
# device = t.device("cpu")


def run_demo(img1_path, img2_path, img_width, img_height, path_to_model):
    IMAGE_WIDTH = img_width
    IMAGE_HEIGHT = img_height
    MODEL_PATH = path_to_model
    IMG1_PATH = img1_path
    IMG2_PATH = img2_path
    # -------------------------------
    WIDTH = 512  # - 8
    PAD = 31
    FRACTION = 8
    OUTPUT_SIZE = WIDTH // FRACTION
    CROP_SIZE = WIDTH - FRACTION
    LAYER_POOL = False
    FILTER_SIZE = 3
    EMB_CHANNELS = 256
    RESIDUALS = 0

    size_frac = WIDTH / IMAGE_WIDTH
    transform = Resize(int(IMAGE_HEIGHT * size_frac))
    fraction_resized = int(FRACTION / size_frac)
    # --------------------------------

    model = get_parametrized_model(LAYER_POOL, FILTER_SIZE, EMB_CHANNELS, RESIDUALS, PAD, device)
    model = load_model(model, MODEL_PATH)

    model.eval()
    with torch.no_grad():
        # print(read_image(IMG1_PATH).shape)
        # print(read_image(IMG2_PATH).shape)
        # print(IMG1_PATH)
        # print(IMG2_PATH)
        if read_image(IMG1_PATH).shape[0] == 3 and read_image(IMG2_PATH).shape[0] == 3:
            source, target = transform(read_image(IMG1_PATH) / 255.0).to(device), \
                             transform(read_image(IMG2_PATH) / 255.0).to(device)[..., FRACTION//2:-FRACTION//2]

        # print(source.shape, target.shape)
            histogram = model(source.unsqueeze(0), target.unsqueeze(0), padding=PAD)
        # histogram = (histogram - t.mean(histogram)) / t.std(histogram)
        # histogram = t.softmax(histogram, dim=1)

            histogram_max = torch.max(histogram).cpu()


        # # visualize:
        # shift_hist = histogram.cpu()
        # f = interpolate.interp1d(np.linspace(0, IMAGE_WIDTH, OUTPUT_SIZE), shift_hist, kind="cubic")
        # interpolated = f(np.arange(IMAGE_WIDTH))
        # ret = -(np.argmax(interpolated) - IMAGE_WIDTH // 2.0)
        # plot_displacement(source.squeeze(0).cpu(),
        #                   target.squeeze(0).cpu(),
        #                   shift_hist.squeeze(0).cpu(),
        #                   displacement=None,
        #                   importance=None,
        #                   name="result",
        #                   dir="./")
        # print("Estimated displacement is", ret, "pixels.")

            return histogram_max


if __name__ == '__main__':
    run_demo()
