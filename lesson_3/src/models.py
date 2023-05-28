from pathlib import Path
import gdown

segment_model_file = 'static/segment.h5'
mnist_model_file = 'static/model_mnist.h5'


def download_models():

    # 1. скачиваем модель для сегментации
    segment_model_path = Path(segment_model_file)

    if not segment_model_path.exists():
        url = "https://drive.google.com/uc?id=1qYPTvbiu4TFnL5g2YNl2XmTPK7LW5AjH"

        print(f"download {segment_model_file} from {url}")

        gdown.download(url, segment_model_file, quiet=False)
    else:
        print(f"{segment_model_file} local exist")

    # 2. скачиваем модель для mnist
    mnist_model_path = Path(mnist_model_file)

    if not mnist_model_path.exists():
        url = "https://drive.google.com/uc?id=181HJXAcq_VE7Ta4MUCsbFsbd8qR3jz9F"

        print(f"download {mnist_model_file} from {url}")

        gdown.download(url, mnist_model_file, quiet=False)
    else:
        print(f"{mnist_model_file} local exist")

