author: Jin Jay
title: 光线追踪
Date: 2016-04
description: 计算机图形学课程作业，光线追踪模拟。
keywords: 光线追踪
          ray trace
          javascript


<h1> <center>光线追踪</center> </h1>
<!-- 画布 -->
<canvas id="paper"  height="300"></canvas>
<script type="text/javascript">
var ctx;    // 绘制context
var pixels; // 像素点
var screen_width = 320; // 宽
var screen_height = 200; // 高
var frame = 0;   // 帧

// 初始化
function init() {
    ctx = document.getElementById('paper').getContext('2d');
    pixels = ctx.createImageData(screen_width, screen_height);
    setInterval(draw, 1000 / 25);
};
// 绘制
function draw() {
    computeScene(); // 旋转物体后重新计算场景
    ctx.putImageData(pixels, 0, 0);
    // 通过frame更新位置
    frame++;
};

/* 向量类
 * 默认初始化为(0,0,0)
 * 
 */
function Vector(x,y,z) {
    if (arguments.length == 0) {
        x = y = z = 0;
    }
    this.x = x;
    this.y = y;
    this.z = z;
}
Vector.prototype = {
    // 设置x, y, z
    set: function(x,y,z) {
        this.x = x;
        this.y = y;
        this.z = z;
    },
    // 向量长度
    magnitude: function() {
        return Math.sqrt(this.x*this.x + this.y*this.y + this.z*this.z);
    },
    // 归一化
    normalize: function() {
        var m = this.magnitude();
        if (m == 0) m = 1;
        this.x /= m;
        this.y /= m;
        this.z /= m;
        return this;
    }
}

/* 光线
 * origin: 源点
 * direction: 方向
 */
function Ray() {
    this.origin = new Vector();
    this.direction = new Vector();
}
/* Sphere
 * center: 中心点，radius: 半径
 */
function Sphere() {
    this.type = "sphere";
    this.center = new Vector();
    this.radius = 1.0;
}
Sphere.prototype = {
    // 球体上一点的法线
    normalToPoint: function(x,y,z) {
        x -= this.center.x;
        y -= this.center.y;
        z -= this.center.z;
        // 归一化 
        x /= this.radius;
        y /= this.radius;
        z /= this.radius;
        return {x: x, y: y, z: z};
    },
    /* 球面求交
     * 输入参数: ray
     * 返回值: type和dist(距离).
     * Type的值:
     * 0: 无交点
     * 1: 相交，交点在球体内部
     * 2: 相交，焦点在球体外部
     * 注意，ray的direction需要归一化
     */
    intersect: function(ray) {
        var x, y, z, distance = +Infinity;
        // 光线源点到射线的向量
        x = this.center.x - ray.origin.x;
        y = this.center.y - ray.origin.y;
        z = this.center.z - ray.origin.z;
        // (x,y,z)·(x, y, z)
        var xyz_dot = (x*x)+(y*y)+(z*z);
        /* compute dot product between x,y,z and ray direction. */
        var b = (x*ray.direction.x)+(y*ray.direction.y)+(z*ray.direction.z);
        /* We can now compute the discriminant and check for intersections. */
        var disc = b*b - xyz_dot + this.radius*this.radius;
        var type = 0;
        if (disc > 0) {
            var d = Math.sqrt(disc);
            var root1 = b-d;
            var root2 = b+d;
            if (root2 > 0) {
                if (root1 < 0) {
                    if (root2 < distance) { distance = root2; type = -1; }
                } else {
                    if (root1 < distance) { distance = root1; type = 1; }
                }
            }
        }
        return {type: type, dist: distance};
    }
}
/* 平面
 * 三个点确定一个平面
 */
function Plane(x1,y1,z1,x2,y2,z2,x3,y3,z3) {
    /* 平面内部表示为:
     * ax + by + cz + d = 0
     * (a, b, c)为平面的法线
     */
    var v1x = x1-x2, v1y = y1-y2, v1z = z1-z2;
    var v2x = x1-x3, v2y = y1-y3, v2z = z1-z3;

    // 法线
    var nx = (v1y*v2z)-(v1z*v2y);
    var ny = (v1z*v2x)-(v1x*v2z);
    var nz = (v1x*v2y)-(v1y*v2x);

    // 代入一点坐标求解d
    this.normal = new Vector(nx,ny,nz);
    this.d = -(nx*x1 + ny*y1 + nz*z1);
}
Plane.prototype = {
    normalToPoint: function(x,y,z) {
        return this.normal;
    },
    intersect: function(ray) {
        var type = 0;
        var distance = +Infinity;
        // 首先检查是否与平面相交
        var ndotrd = (this.normal.x * ray.direction.x) +
                     (this.normal.y * ray.direction.y) +
                     (this.normal.z * ray.direction.z);
        if (ndotrd) {
            // 计算交点距离
            var ndoro = (this.normal.x * ray.origin.x) +
                        (this.normal.y * ray.origin.y) +
                        (this.normal.z * ray.origin.z);
            distance = - (ndoro + this.d)/ndotrd;
            /* Now there is an intersection only if the distance is positive,
               otherwise the intersection is not in the ray direction
               (but is backward). */
            if (distance > 0) type = 1;
        }
        return {type: type, dist: distance};
    }
}
// 灯光
function Light() {
    this.type = "light";
    this.center = new Vector();
}
// 物体
function Solid(name,o) {
    this.name = name;
    this.o = o;
    this.color = {r: 1, g: 1, b: 1};
    this.specularity = 0;
    this.reflection = 0;
}
// 场景
function Scene() {
    this.objects = [];
    this.lights = [];
}
Scene.prototype = {
    addObject: function(o) {
        this.objects.push(o);
        return o;
    },
    addLight: function(o) {
        this.lights.push(o);
        return o;
    },
    traceRay: function (ray, depth) {
        var obj = null;
        var color = {r: 0, g: 0, b: 0};
        var distance = +Infinity;
        for (var j = 0; j < this.objects.length; j++) {
            var test_obj = this.objects[j];
            var res = test_obj.o.intersect(ray);
            if (res.type) {
                if (obj == null || res.dist < distance) {
                    obj = test_obj;
                    distance = res.dist;
                }
            }
        }
        // 如果碰到了物体，求解颜色
        if (obj) {
            // 求解交点
            var x = ray.origin.x + ray.direction.x*distance,
                y = ray.origin.y + ray.direction.y*distance,
                z = ray.origin.z + ray.direction.z*distance;
            // 交点处的法线
            var normal = obj.o.normalToPoint(x,y,z);
            for (var j = 0; j < this.lights.length; j++) {
                var light = this.lights[j];
                // 计算光线到交点的向量
                var lx = light.o.center.x - x;
                var ly = light.o.center.y - y;
                var lz = light.o.center.z - z;
                // 归一化
                var len = Math.sqrt(lx*lx + ly*ly + lz*lz);
                if (len == 0) len = 1;
                lx /= len;
                ly /= len;
                lz /= len;
                // 阴影计算
                var pldistance = Math.sqrt(
                    (x-light.o.center.x)*(x-light.o.center.x)+
                    (y-light.o.center.y)*(y-light.o.center.y)+
                    (z-light.o.center.z)*(z-light.o.center.z));
                var sray = new Ray();

                sray.origin.set(x,y,z);
                // 增加一小点，避免光线与当前点相交
                sray.origin.x += lx/10000;
                sray.origin.y += ly/10000;
                sray.origin.z += lz/10000;
                sray.direction.set(lx, ly, lz);
                var shadow = false;

                for (var i = 0; i < this.objects.length; i++) {
                    var test_obj = this.objects[i];
                    var res = test_obj.o.intersect(sray);
                    if (res.type && res.dist < pldistance) {
                        shadow = true;
                        break;
                    }
                }
                if (shadow) continue; // 如果被遮挡，则计算下一个光线
                // 漫反射 
                var cosine = normal.x*lx+normal.y*ly+normal.z*lz;
                if (cosine < 0) cosine = 0;
                color.r += cosine * obj.color.r * light.color.r;
                color.g += cosine * obj.color.g * light.color.g;
                color.b += cosine * obj.color.b * light.color.b;
                // 折射
                if (obj.specularity > 0) {
                    var vrx = lx - normal.x * cosine * 2,
                        vry = ly - normal.y * cosine * 2,
                        vrz = lz - normal.z * cosine * 2;
                    var cosSigma = (ray.direction.x*vrx)+
                                   (ray.direction.y*vry)+
                                   (ray.direction.z*vrz);
                    if (cosSigma > 0) {
                        var specularity = obj.specularity;
                        color.r += light.color.r * specularity * Math.pow(cosSigma,64);
                        color.g += light.color.g * specularity * Math.pow(cosSigma,64);
                        color.b += light.color.b * specularity * Math.pow(cosSigma,64);
                    }
                }
                // 镜面反射
                if (obj.reflection > 0 && depth < 3) {
                    var rr = new Ray();
                    var dotnr = (ray.direction.x * normal.x) +
                                (ray.direction.y * normal.y) +
                                (ray.direction.z * normal.z);
                    rr.origin.set(x,y,z);
                    rr.direction.set(ray.direction.x - 2 * normal.x * dotnr,
                                     ray.direction.y - 2 * normal.y * dotnr,
                                     ray.direction.z - 2 * normal.z * dotnr);
                    rr.origin.x += rr.direction.x / 10000;
                    rr.origin.y += rr.direction.y / 10000;
                    rr.origin.z += rr.direction.z / 10000;
                    var rcolor = this.traceRay(rr,depth+1);
                    color.r *= 1-obj.reflection;
                    color.g *= 1-obj.reflection;
                    color.b *= 1-obj.reflection;
                    color.r += rcolor.color.r * obj.reflection;
                    color.g += rcolor.color.g * obj.reflection;
                    color.b += rcolor.color.b * obj.reflection;
                }
            }
            if (color.r > 1) color.r = 1;
            if (color.g > 1) color.g = 1;
            if (color.b > 1) color.b = 1;
        }
        return {obj: obj, color: color}
    },
    traceScene: function (camera) {
        var ray = new Ray();
        ray.origin = camera.position;
        for (var x = 0; x < screen_width; x++) {
            for (var y = 0; y < screen_height; y++) {
                ray.direction.set((x-screen_width/2)/100,
                                  (y-screen_height/2)/100,
                                  4);
                ray.direction.normalize();
                var trace = this.traceRay(ray,0);
                var offset = x*4+y*4*screen_width;
                pixels.data[offset+3] = 255;
                pixels.data[offset+0] = trace.color.r*255;
                pixels.data[offset+1] = trace.color.g*255;
                pixels.data[offset+2] = trace.color.b*255;
            }
        }
    }
}
function Camera() {
    this.position = new Vector();
    this.transfrom = null;
}

// 场景
var scene = new Scene();
var sphere1 = scene.addObject(new Solid("Sphere 1",new Sphere()));
var sphere2 = scene.addObject(new Solid("Sphere 2",new Sphere()));
var plane = scene.addObject(new Solid("Ground",new Plane(0,.5,-2,0,.5,-4,2,.5,-2)));
var light1 = scene.addLight(new Solid("Light 1",new Light()));
var light2 = scene.addLight(new Solid("Light 2",new Light()));
var light3 = scene.addLight(new Solid("Light 3",new Light()));
var camera = new Camera();

sphere1.o.radius = 0.5;

sphere2.o.center.x = 0;
sphere2.o.radius = 0.5;
light1.o.center.set(4,-1,-2);
light2.o.center.set(-1,-1,-2);
light3.o.center.set(1,-6,-2);
light1.color.r = .5;
light1.color.g = .5;
light1.color.b = .5;
light2.color.r = .3;
light2.color.g = .3;
light2.color.b = .3;
light3.color.r = .4;
light3.color.g = .4;
light3.color.b = .4;
sphere1.color.r = 1;
sphere1.color.g = .3;
sphere1.color.b = .3;
sphere1.specularity = .5;
sphere1.reflection = .1;
sphere2.color.r = .3;
sphere2.color.g = 1;
sphere2.color.b = .3;
sphere2.specularity = .5;
sphere2.reflection = .1;
plane.color.r = .3;
plane.color.g = .3;
plane.color.b = .3;

camera.position = new Vector(0, 0, -4);

function computeScene() {
    sphere1.o.center.x = Math.cos(frame/10);
    sphere1.o.center.z = Math.sin(frame/10);
    scene.traceScene(camera);
}
init();
</script>

# 光线追踪设计

[TOC]