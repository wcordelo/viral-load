# viral-load
HST.426 Viral Load Project
The Viral Load Project for HST.426 allows users to use a Blynk app to control a linear actuator motor, take pictures, and use a machine learning algorithm (using OpenCV) to calculate the number of cells in a virus plaque assay. 

## Getting Started

The following is needed to have the viral load contraption fully functional

1) [Raspberry Pi 3 Model B](https://www.amazon.com/Raspberry-Pi-RASPBERRYPI3-MODB-1GB-Model-Motherboard/dp/B01CD5VC92/ref=sr_1_3?s=pc&ie=UTF8&qid=1526361583&sr=1-3&keywords=raspberry+pi+3)
2) [Linear Actuator Motor](https://www.amazon.com/gp/product/B01L6W1GRG/ref=ox_sc_act_title_3?smid=A16P4TUM521SQ8&psc=1)

### Installing

Please install the following software
1) [Raspberry N00BS](https://www.raspberrypi.org/downloads/noobs/) - The operating software for Raspberry Pi
2) [OpenCV](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/) - OpenCV
3) Blynk Software (from the App Store on your Mobile Phone)
4) Python

### Running the Code

To run the code

```
python camera.py
```
This runs the arduino app on your mobile phone which is linked to the python script. Calling the camera function takes a picture and saves it in the photos directory. You can access the photos on your directory anytime.

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **William Lopez-Cordero** - [wcordelo](https://github.com/wcordelo)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
