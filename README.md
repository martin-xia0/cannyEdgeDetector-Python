# cannyEdgeDetector-Python
use the code by typing this on terminal:

 python cannycode.py --image /magepath/image.jpg

A implementation of canny edge detection algorithm in python using numpy and opencv.

There are variety of methods for edge detection in a image which focus on identifying the change in brightness level of pixels as sharp or gradual. The sharp change is edge. The various methods using kernals are Prewitt, Sobel, Robert cross and canny to name a few. While the first three work by using kernals with different weights, canny  uses a computational apporoach to detect edges. This algorithm is also adaptable  to various environment by virtue of its parameters. This makes canny more efficient and favourite among all of them.

Algorithm: Canny edge detector is a muti-step algorithm that detects edges in a image.The steps of canny edge detection are as follows.

1.Noise removal by Gaussian Filter: We are going to compute gradient information of our images in the upcoming steps, and the Prewit/Sobel kernals that we are going to use are sensitive to noise. So we will filter out the noise with gaussian filter of size 5x5. If we increase the filter size, we tend to loose some useful edge information. Also the position of the computed edge appears to be shifted. This is refered to as localization error. If we want some fine information, we can take a kernal with small size. (3x3)

2.Finding intensities gradients of the image: The edge pixels in the image will have different directions. To compute the gradient, we use first derivative in horizontal Gx and vertical direction Gy. Then we will compute the phase(angle) and magnitude(gradient) from this information.      

Once we have the angle information, we need to quantize all the angle values to 0, 45, 90 or 135 degrees.

3.Non-maximum suppression: The image computed now has thicker edges. So we apply non maximum suppression on all the edges to obtain a single pixel thick edge. This is done by kepping the pixel which has a highest value in its neighbourhood in the direction of its gradient.

4.Hysteresis Thresholding: We now have a image with lot of false detections which we need to remove. So we do this by deciding two threshold values, a lower threshold and a higher threshold value. 

The pixel value is considered to be a part of a edge if it is connected to a pixel whose value is higher than the maximum threshold. All the edges having pixel values less than the lower threshold values are discarded. The resulting image is a edge image.

Choosing the upper and lower threshold is a bit tricky sometimes, so i have used a little trick which i found in one of the blog i follow for computer vision and image processing tips and tricks long time ago. In the pyimagesearch blog, the author has used a statistical technique to compute the TL and TH value, that is our parameters, by using the highest and lowest pixel value in the gradient image. I tried the same and found a value after some hit and trial for different images.
			                tl  = tl  * max(newgrad)
				        th = th * max(newgrad)

Parameters: The parameters in an algorithm can either increase the speed of the execution or increase the effeciency of the code. The main paramenters in this algorithm are the lower threshold and higher threshold. While the lower threshold decides which pixels are too weak to be a edge, the upper threshold selects the pixels which have a intensity greater than this threshold and identifies the connected pixels as sure edges. Thus the lower threshold helps reducing noise and other less significant non edge information from the image. The upper threshold makes sure that that  more prominent edges appears.

The other parameters that can also be considered to have an impact is the gaussian filters size. Although i have taken a fixed size of 5, but the increase and decrease of this filter size can cause decrease and increase  in the number of edges found respectively.
 
Applications:There are various applications of edge detection.
Structural and Shape analysis, Boundary detection, Edge Descriptor(As a feature), Image segmentation and many more.
