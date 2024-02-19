import os
support_img_ext = ['bmp', 'dng', 'jpeg', 'jpg', 'mpo', 'png', 'tif', 'tiff', 'webp', 'pfm', 'JPG'] 
support_vid_ext = ['asf', 'avi', 'gif', 'm4v', 'mkv', 'mov', 'mp4', 'mpeg', 'mpg', 'ts', 'wmv', 'webm']
support_model_ext = ['torchscript', 'pt', 'onnx', 'engine', 'mlmodel', 'pb', 'tflite']
#Рандомные улицы
street = ['Ushakova', 'Kirovogradskaia', 'Naximova', 'Zakamskaia', 'Ribalko', 'Astraxanskaia']

model_path = "Resources/YoloB32E30_v2.pt"

ImagesSavedPath = os.path.join(os.getcwd(), 'results')