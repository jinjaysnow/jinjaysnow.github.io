author: Jin Jay
title: iOS Capture EAGLView
Date: 2015-02
description: iOS capture EAGLView as UIImage/snapshot EAGLView.
keywords:   iOS7, iOS8 
			EAGLView
			snapshot OpenGLES view

## snapshot view/EAGLView in iOS7 or later
	
	- (void)snapshot:(UIView *view){
	    UIGraphicsBeginImageContext(view.frame.size);
	    [self drawViewHierarchyInRect:view.frame afterScreenUpdates:YES];
	    UIImage *image = UIGraphicsGetImageFromCurrentImageContext();
	    UIGraphicsEndImageContext();
	    UIImageWriteToSavedPhotosAlbum(image, nil, nil, nil);
	}


[TOC]