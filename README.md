# Image_stitching
Given a set of images of different views taken from different angles/view points. The program groups them together to in order to perform global image alignment and stitching.


The current implemation is limited to grouping of images into sets of views. Global Image alingment and stitching has not been addressed yet.



Requirments:
  1. OpenCV3
  2. Python3.5 or >
  
 
Run:
The main script is find_views.py in source directory. The script need path to directory containing images.
More information can be found using find_views.py -h

Approch:
The current approch use ORB features to find set of images with belong to the same view. After staring with a random images it expands the list with next best possible match to that image. The present method groups the images in a view with high accuracy. The current algorithm ensures very less false matching.
The approch can further be extended as follows:

1. For each each image in each view find the best possible match and create a graph structure with homography as edge weight.
2. Do global alingment, techniques like joint cost minimization, Bundle adjustment can be implemented.
3. Once you have alingment stitching can be accomplished using the homography.

Current Pitfalls:
The current algorithm is very basic and just does feature based maching. Thus a few images which needed to be part of a particular view may not included.

Possible approches to tackle current pitfall:
1. Rather than finding all the matches for a particular image and adding it to current view only find the image with best match and expand from there. But there might be cases where this approch might fail.


Future Improvements:
1. validate maching based on on featureless techniques like pixel based statistics.
2. Use intensity/color histogram to find paches in image with similar intensity. 
Extend current algorithm to form composite images.
