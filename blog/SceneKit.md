author: Jin Jay
title: SceneKit与OpenGL结合
Date: 2015-03
description: 介绍iOS上的SceneKit与OpenGLES集成————个人使用Vuforia时遇到的一个问题。
keywords: iOS SceneKit, iOS OpenGLES, SceneKit OpenGL

### 第一步，初始化EAGLContext、SCNScene和SCNRenderer

    EAGLContext *context = [[EAGLContext alloc] initWithAPI:kEAGLRenderingAPIOpenGLES2];
	SCNScene *scnScene = [SCNScene sceneName:@"example.dae"];
	SCNRenderer *scnRender = [SCNRenderer rendererWithContext:(void *)context option:nil];


### 第二步，在OpenGLES渲染帧之间渲染场景

	[EAGLContext setCurrentContext: context];
	glBindFramebuffer(GL_FRAMEBUFFER, defaultFramebuffer);

	...// OpenGLES 操作

	...// SceneKit 操作
	[scnRender render]; // 渲染SceneKit场景
	
	glBindRenderbuffer(GL_RENDERBUFFER, colorRenderbuffer);
	[context presentRenderbuffer:GL_RENDERBUFFER];

[TOC]