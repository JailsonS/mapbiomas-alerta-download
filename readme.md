# API consumer for Mapbiomas Alert Data
This is a short script aimed to download deforestation data of Mapbiomas Alerta project. 
(https://alerta.mapbiomas.org/). In order to use this code you will need the follow requirements:

### Mapbiomas Alerta account
Mapbiomas alerta data is free and is available to anyone but you have to create an account to 
download the data.
+ access the link below and create your account
```
https://plataforma.alerta.mapbiomas.org/sign-in
```

### Clone repository
Clone this repository
```
git clone https://github.com/JailsonS/mapbiomas_alerta_consumer.git
```

### Install dependencies 
Create virtual env
```
python -m venv venv
```


Activate your vitual env
```
# for windows 
C:\> <venv>\Scripts\activate.bat

# for linux 
source <venv>/bin/activate
```

Install dependencies
```
pip install -r requirements.txt
```

### Run code 
From root repository, run the below code to download PNG file:
```
python ./src/get_png_images.py --email [your-email] --password [your-password] --alert_code [alertcode] --save_path [output-path]
```
Then, you can run the following code to remove lengend and background:
```
python ./src/get_png_images_cropped.py --input_img [dir-image-name] --output_img [dir-image-name]
```