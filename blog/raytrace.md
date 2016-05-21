author: Jin Jay
title: 光线追踪
Date: 2016-04
description: 计算机图形学课程作业，光线追踪模拟。
keywords: 光线追踪
          ray trace
          javascript


<h1> <center>光线追踪</center> </h1>
<!-- 画布popup -->
<style type="text/css">
.box {
  width: 40%;
  margin: 0 auto;
  background: rgba(255,255,255,0.2);
  padding: 35px;
  border: 2px solid #fff;
  border-radius: 20px/50px;
  background-clip: padding-box;
  text-align: center;
}

.button {
  font-size: 1em;
  padding: 10px;
  color: #000;
  border: 2px solid #06D85F;
  border-radius: 20px/50px;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s ease-out;
}
.button:hover {
  background: #06D85F;
}

.overlay {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7);
  transition: opacity 500ms;
  visibility: hidden;
  opacity: 0;
  z-index: 1000;
}
.overlay:target {
  visibility: visible;
  opacity: 1;
}

.popup {
  margin: 130px auto;
  padding: 20px;
  background: #fff;
  border-radius: 5px;
  width: 80%;
  position: relative;
  transition: all 5s ease-in-out;
}

.popup h2 {
  margin-top: 0;
  color: #333;
  font-family: Tahoma, Arial, sans-serif;
}
.popup .close {
  position: absolute;
  top: 20px;
  right: 30px;
  transition: all 200ms;
  font-size: 30px;
  font-weight: bold;
  text-decoration: none;
  color: #333;
}
.popup .close:hover {
  color: #06D85F;
}
.popup .content {
  max-height: 80%;
  overflow: auto;
}

@media screen and (max-width: 700px){
  .box{
    width: 70%;
  }
  .popup{
    width: 70%;
  }
}
</style>

<div class="box">
    <a class="button" href="#popup1" onclick="resume();">启动光线追踪动画</a>
</div>

<div id="popup1" class="overlay">
    <div class="popup">
        <h2>光线追踪实时渲染</h2>
        <a class="close" href="#" onclick="stop();">&times;</a>
        <div class="content">
            <center>
                <canvas id="paper"  height="200"></canvas>
            </center>
        </div>
    </div>
</div>

<!-- <center>
    <canvas id="paper"  height="200"></canvas>
</center>
 -->
<script type="text/javascript">
var ctx;    // 绘制context
var pixels; // 像素点
var screen_width = 320; // 宽
var screen_height = 200; // 高
var frame = 0;   // 帧
var animate = 0; // 是否动画

// 初始化
function init() {
    ctx = document.getElementById('paper').getContext('2d');
    pixels = ctx.createImageData(screen_width, screen_height);
};
// 绘制
function draw() {
    computeScene(); // 旋转物体后重新计算场景
    ctx.putImageData(pixels, 0, 0);
    // 通过frame更新位置
    frame++;
    if (animate) {
        setTimeout(draw, 1000/25);
    };
};
// 暂停
function stop() {
    animate = 0;
}
// 恢复
function resume() {
    animate = 1;
    setTimeout(draw, 1000);
}

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
    },
    // 点乘
    dot_product: function(v) {
        return (this.x*v.x + this.y*v.y + this.z*v.z);
    },
    // 减法
    sub: function(v) {
        var r = new Vector(this.x-v.x, this.y-v.y, this.z-v.z);
        return r;
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
     * 1: 相交，视点在球体内部
     * -1: 相交，视点在球体外部
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
        var b = (x*ray.direction.x)+(y*ray.direction.y)+(z*ray.direction.z);
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
            // 只有距离为正值时才会相交
            if (distance > 0) type = 1;
        }
        return {type: type, dist: distance};
    }
}
/* 多面体
 * 通过data构造形状
 * vertices, 顶点坐标;
 * faces, 面的顶点索引数组;(一个面由多个顶点组成) 
 * center, 中心点，作为多面体的内部的一点，用于对物体进行变换
 * transform, 物体的变换，平移旋转等操作
 */
function Geometry(data) {
    this.type = 'Geometry';
    this.center = data['center'];
    this.vertices = data['vertices'];
    this.faces = data['faces'];
    this.faces_plane = [];

    for (var i = 0; i <= data['faces'].length - 1; i++) {
        var f = data['faces'][i];
        var v0 = data['vertices'][ f[0] ];
        var v1 = data['vertices'][ f[1] ];
        var v2 = data['vertices'][ f[2] ];
        this.faces_plane[i] = new Plane(v0[0], v0[1], v0[2],
                                        v1[0], v1[1], v1[2],
                                        v2[0], v2[1], v2[2]);
    };
    // 求解最大的包围半径
    this.radius = -Infinity;
    for (var i = data['vertices'].length - 1; i >= 0; i--) {
        var v = data['vertices'][i];
        var c = data['center'];
        var vc = new Vector(v[0] - c[0], v[1] - c[1], v[2] - v[2]);
        var l = vc.magnitude();
        this.radius = this.radius > l ? this.radius : l;
    };
    this.transform = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ];
};
function getQuadrant(x, y) {
    if (x >= 0 && y >= 0)
        return 0;
    else if (x < 0 && y >= 1)
        return 1;
    else if (x < 0 && y < 0)
        return 2;
    else
        return 3;
}
var signTable = [
    [ 0,  1,  2, -1],
    [-1,  0,  1,  2],
    [ 2, -1,  0,  1],
    [ 1,  2, -1,  0]
];
function transformMulTransform(t1, t2) {
    var result = [];
    for (var i = 0; i < 3; i++) {
        var t = [];
        t[0] = t1[i][0]*t2[0][0] + t1[i][1]*t2[1][0] + t1[i][2]*t2[2][0];
        t[1] = t1[i][0]*t2[0][1] + t1[i][1]*t2[1][1] + t1[i][2]*t2[2][1];
        t[2] = t1[i][0]*t2[0][2] + t1[i][1]*t2[1][2] + t1[i][2]*t2[2][2];
        result[i] = t;
    };
    return result;
};
function xyzMultTransform(xyz, transform) {
    var result = [];
    result[0] = xyz[0]*transform[0][0] + xyz[1]*transform[1][0] + xyz[2]*transform[2][0];
    result[1] = xyz[0]*transform[0][1] + xyz[1]*transform[1][1] + xyz[2]*transform[2][1];
    result[2] = xyz[0]*transform[0][2] + xyz[1]*transform[1][2] + xyz[2]*transform[2][2];
    return result;
};
Geometry.prototype = {
    makeTransform: function() {
        this.center = xyzMultTransform(this.center, this.transform);
        for (var i = this.vertices.length - 1; i >= 0; i--) {
            this.vertices[i] = xyzMultTransform(this.vertices[i], this.transform);
        };
        this.buildPlanes();
    },
    // 构造面所在的平面，及包围球体
    buildPlanes: function() {
        this.faces_plane = [];
        for (var i = 0; i <= this.faces.length - 1; i++) {
            var f = this.faces[i];
            var v0 = this.vertices[ f[0] ];
            var v1 = this.vertices[ f[1] ];
            var v2 = this.vertices[ f[2] ];
            this.faces_plane[i] = new Plane(v0[0], v0[1], v0[2],
                                            v1[0], v1[1], v1[2],
                                            v2[0], v2[1], v2[2]);
        };
        for (var i = this.vertices.length - 1; i >= 0; i--) {
            var v = this.vertices[i];
            var c = this.center;
            var vc = new Vector(v[0] - c[0], v[1] - c[1], v[2] - v[2]);
            var l = vc.magnitude();
            this.radius = this.radius > l ? this.radius : l;
        };
    },
    // 求解交点法线
    normalToPoint: function(x, y, z) {
        var index = 0;
        var distance = +Infinity;

        for (var i = this.faces_plane.length - 1; i >= 0; i--) {
            var p_n = this.faces_plane[i].normal;
            var p_d = this.faces_plane[i].d;
            // if (Math.abs(x*p_n.x + y*p_n.y + z*p_n.z + p_d) < 1e-16) {
            //     planes.push(this.faces_plane[i]);
            // };
            var p_distance = Math.abs(x*p_n.x + y*p_n.y + z*p_n.z + p_d);
            if (distance > p_distance) {
                distance = p_distance;
                index = i;
            };
        };
        if (distance > 1e-6) {
            console.log(distance);
        };
        return this.faces_plane[index].normal;
    },
    intersect: function(ray) {
        var type = 0;
        var distance = +Infinity;

        // 光线源点到中心的向量
        x = this.center[0] - ray.origin.x;
        y = this.center[1] - ray.origin.y;
        z = this.center[2] - ray.origin.z;
        // (x,y,z)·(x,y,z)
        var xyz_dot = (x*x)+(y*y)+(z*z);
        // (x,y,z)·(rdx,rdy,rdz)
        var b = (x*ray.direction.x)+(y*ray.direction.y)+(z*ray.direction.z);
        // 看是否与外围球体相交
        var disc = b*b - xyz_dot + this.radius*this.radius;
        if (disc > 0) {
            var result = [];
            for (var i = 0; i <= this.faces_plane.length - 1; i++) {
                // 先看是否与每一个平面相交
                var p = this.faces_plane[i];
                result[i] = p.intersect(ray);
                if (result[i].type == 1) {
                    // 检查是否在多边形内部，使用改进的弧长法
                    var f = this.faces[i];
                    distance = result[i].dist;
                    var px = ray.origin.x + ray.direction.x*distance,
                    py = ray.origin.y + ray.direction.y*distance;

                    // 该平面点的分布
                    var coord = [];
                    for (var j = 0; j < f.length; j++) {
                        var v = this.vertices[ f[j] ];
                        var deltax = v[0] - px, deltay = v[1] - py;
                        coord[j] = [deltax, deltay];
                    };
                    coord[f.length] = coord[0]; // coord中存放的是移动坐标系后的顶点的坐标

                    var n = 0;
                    var on_line = false;
                    for (var j = 1; j <= coord.length - 1; j++) {
                        // 获取点所在的象限
                        var g0 = getQuadrant(coord[j-1][0], coord[j-1][1]);
                        var g1 = getQuadrant(coord[j][0], coord[j][1]);
                        // 弧长增量
                        var addition = signTable[g0][g1];
                        if (addition == 2) {
                            var f = coord[j][1] * coord[j-1][0] - coord[j][0]*coord[j-1][1];
                            if (f > 0) {
                                addition = 2;
                            } else if (f == 0) {
                                on_line = true;
                                break;
                            } else {
                                addition = -2;
                            }
                        };
                        n += addition;
                    };
                    if (n == 0 && on_line) {
                        result[i].type = 0;
                    };
                };
            };
            for (var i = result.length - 1; i >= 0; i--) {
                if (result[i].type != 0) {
                    type = result[i].type;
                    // type = -1;
                    distance = (distance > result[i].dist) ? result[i].dist : distance;
                };
            };
            // if (type != 0) {
            //     // 光源在内部还是外部

            // };
        };
        return {type: type, dist: distance};
    }
}
// 灯光
function Light() {
    this.type = "light";
    this.center = new Vector();
}
// 物体
function Solid(name, o) {
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
                // ray.direction.set((x-screen_width/2)/100,
                //                   (y-screen_height/2)/100,
                //                   camera.focus);
                // ray.direction = xyzMultTransform(ray.direction, camera.transform);
                var direction = [(x-screen_width/2)/100,
                                  (y-screen_height/2)/100,
                                  camera.focus];
                direction = xyzMultTransform(direction, camera.transform);
                ray.direction.set(direction[0], direction[1], direction[2]);
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
    this.transform = [[1,0,0,0],
                      [0,1,0,0],
                      [0,0,1,0],
                      [0,0,0,1]];
    this.focus = 4.0;
}

// 场景
var scene = new Scene();
var sphere1 = scene.addObject(new Solid("Sphere 1",new Sphere()));
var sphere2 = scene.addObject(new Solid("Sphere 2",new Sphere()));
var g_data = {
    'center': [0, 1, 0],
    'vertices': [[-1, 0, -1], [1, 0, -1], [1, 0, 1], [0, 0, 1],
                 [-2, 2, -2], [2, 2, -2], [2, 2, 2], [-2, 2, 2]],
    'faces': [[0, 1, 2, 3], [0, 1, 5, 4], [1, 2, 6, 5],
              [4, 5, 6, 7], [0, 3, 7, 4], [2, 3, 7, 6]],
};

var geometry = new Geometry(g_data);
var scale_t = [
    [0.1, 0, 0],
    [0, 0.1, 0],
    [0, 0, 0.1]
];
geometry.transform = transformMulTransform(geometry.transform, scale_t);
geometry.makeTransform();
// var gg = scene.addObject(new Solid("Geometry", geometry));
// gg.color.r = 1;
// gg.color.g = .5;
// gg.color.b = .5;
// gg.specularity = .5;
// gg.reflection = .3;

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

// 绕Y轴旋转矩阵
function makeRotateY(angle) {
    var sin_theta = Math.sin(angle / 180.0 * Math.PI);
    var cos_theta = Math.cos(angle / 180.0 * Math.PI);
    return [[1.0, 0.0, 0.0, 0.0],
            [0.0, cos_theta, -sin_theta, 0.0],
            [0.0, sin_theta, cos_theta, 0.0],
            [0.0, 0.0, 0.0, 1.0]];
}
// 动画过程
function computeScene() {
    var p = parseInt(frame / 36);
    if ( p == 0 || p == 3) {
        var angle =  5.0 * frame * Math.PI / 180.0;
        sphere1.o.center.x = Math.cos(angle);
        sphere1.o.center.z = Math.sin(angle);
        // 旋转摄像机
        if (frame < 18) {
            var theta = -5 * frame * Math.PI / 180.0;
            camera.position.y = 4.0 * Math.sin(theta);
            camera.position.z = -4.0 * Math.cos(theta);
            camera.transform = makeRotateY( 5 * frame);
        } else if (frame < 36) {
            var theta = -5 * (36 - frame) * Math.PI / 180.0;
            camera.position.y = 4.0 * Math.sin(theta);
            camera.position.z = -4.0 * Math.cos(theta);
            camera.transform = makeRotateY( 5 * (36 - frame));
        };
    } else {
        var zpos = -4;
        if (frame >= 72) {
            z_pos = (frame - 72) / 9.0 - 8;
        } else {
            z_pos = -4 - (frame - 36) / 9.0;
        }
        camera.position.z = z_pos;
    };
    scene.traceScene(camera);
    if (frame >= 143) {
        frame = 0;
    };
}
window.onload = function() {init();};
</script>

# 架构设计
3D成像模型
<center>![ray trace model](../../images/raytrace_model.PNG)</center>
模型中的基本元素：摄像机、场景物体、光源。呈现给用户的是摄像机拍摄到的场景的一部分。

对成像过程进行建模:用户视图是View类，View类包含Camera和Scene，Scene包含Light和Solid。

```
View -|- Camera
      |- Scene -|- Light
                |- Solid
```

下面自顶向下对各个类进行设计。

## View类设计
`View`类管理`Scene`和`Camera`，由`View`类进行成像。
一个`View`可以有多个`Scene`，多个`Camera`。对简单的应用只考虑一个`Scene`和一个`Camera`。
在设定好`Scene`和`Camera`后，由`View`类进行成像过程，故而包含一个`draw`方法。此外`View`类应控制显示视图的大小，故而包含`width`和`height`属性。

|View|
|----|
|width <br> height <br> scene <br> camera|
|draw( )|

## Camera设计
摄像机控制用户观察的位置、角度等。故而`Camera`类包含位置`position`，方向`direction`和焦距`focus`属性。

|Camera|
|----|
|position<br> direction<br> focus|

## Scene设计
一个`Scene`包含多个`Light`和多个`Solid`。`Scene`中运行光线追踪算法，故而包含`raytrace`方法。该方法接收一个视线光线`ray`作为参数，返回颜色值。

|Scene|
|----|
|lights[ ]<br>solids[ ]|
|raytrace( )|

## Light设计
没有光源就不能完成光线追踪过程。在本应用中，仅考虑`Light`为点光源的情况，包含位置`position`和颜色`color`信息。

|Light|
|----|
|position<br>color|

## Solid设计
物体`Solid`是对真实物体的建模，包含形状、颜色、材质等信息。

|Solid|
|----|
|data<br>material<br>color|

`注：data包括物体的形状，位置等信息。`

# 详细设计
## 光线追踪模型
![raytrace](../../images/raytrace.PNG)
投影到视图的光由三部分组成：漫反射光`diffuse`，镜面反射光`Mirror`，折射光`Refraction`。光线追踪从反方向对光进行追踪，使用Phong光照模型，漫反射光的强度与入射角度有关：

```javascript
matte_color = intensity * k * (direction * nomral);
```
其中，intensity为光源光强度，k为漫反射系数(0, 1)之间，direction为光线方向单位向量，normal为法线方向单位向量。

折射光和镜面反射光强度按照Fresnel定律组合:

递归形式的追踪过程伪代码如下：

```javascript
function raytrace(ray, depth) {
    if (depth > MAX_DEPTH) { // 递归的最大深度
        return Color(0, 0, 0); // 到达最大递归深度时返回0值
    }
    interpoint = scene.solids.intersection(ray); // 求解光线与场景中物体的最近交点
    if (interpoint) { // 有交点
        diffuse_color = calculate_diffuse(interpoint); // 求解场景在交点处的漫反射光
        refraction_ray = get_refraction_ray(interpoint, ray); // 求解交点处的折射光线
        refraction_color = raytrace(refraction_ray, depth + 1); // 递归求解折射光颜色
        reflection_ray = get_reflection_ray(interpoint, ray); // 求解交点处的折射光线
        reflection_color = raytrace(reflection_ray, depth + 1); // 递归
        return (diffuse_color + refraction_color + reflection_color); // 返回颜色值
    } else {
        return background_color; // 无交点时返回背景颜色
    }
}
```

分析伪代码，可以发现算法实现中的几个关键点：物体求交，求解折射和反射光线。下面，按照光线追踪的过程进行设计。

###  生成初始入射光线
初始入射光线由`View`类进行生成。先引入光线数据结构。

| Ray |
|-----|
|origin: 光线源点<br>direction: 方向|

其中,`origin`坐标等于`Camera`的position属性。`direction`由下式生成。

$$
direction = \lgroup \frac{x - \frac{width}{2}}{ratio}, \frac{x - \frac{height}{2}}{ratio}, focus \rgroup \cdot transform
$$

其中$width, height$分别为`View`的宽高属性值，$ratio$为三维空间中每单位长度在图像像素平面上占用的像素比率，由`View`控制。$focus$是摄像机的焦距。$transform$是摄像机为中心的坐标系与三维场景空间的坐标系转换矩阵，可以根据`camera`的`direction`属性求解。我们可以通过更改`Camera`的`direction`来生成不同摄像机方向上的图像帧，组合这些图像帧可以得到摄像机移动的动画效果。

###  物体求交
基本流程：对场景中的每一个物体与入射进行求交，如果存在交点就添加到一个临时的交点数组中，接着遍历该数组，得到距离最近的那个交点，及该交点处的相关信息。相关信息包括交点位置，交点处的法线，交点所在的物体颜色信息等等。故而定义求交后的返回信息结构如下：

```javascript
result = {
    point: (0, 0, 0), // 交点坐标
    distance: +Infinity, // 交点到光源点的距离
    normal: (0, 0, 0), // 交点处的法线
    solid: solid, // 交点所在的物体，用于求解折射光线、获取交点处的颜色
}
```

### 计算漫反射光
基本流程：对场景中的每一个光源，计算是否可以直接到达交点(交点与光源的连线不与任何物体相交)。如果可以到达，返回该光源作用于该点的漫反射光颜色；如果不能到达，则该光源在该点的漫反射光作用为0。

计算漫反射的公式如下：

$$diffuse\\_color = solid.color \times \sum^{Lights}\_{light}(light.color \cdot distance \cdot \cos\theta)$$

其中，$solid.color$为物体表面的颜色，$light.color$为光源颜色，$distance$为交点与光源的距离，$\theta$为交点与光源连线与该点处法线的夹角。

### 计算折射光
![折射](../../images/refraction.PNG)
折射光计算需要了解折射面上下的折射率。折射过程满足$\sin\theta\_1\cdot N\_1 = \sin\theta\_2\cdot N\_2$。三维情况下如何求解折射方向？

记单位长度的入射光线方向为$\vec a = (x\_a, y\_a, z\_a)$,单位长度的法线方向为$\vec n = (x\_n, y\_n, z\_n)$,单位长度的折射方向为$\vec b = (x\_b, y\_b, z\_b)$，三个向量在同一个平面内，则有三向量的混合积为0(或者有$\vec B$可以由$\vec A$和$\vec N$表示)有

$$
\begin{cases}
\vec b = \vec a + k \cdot \vec n  \\\\ 
N\_1^2 \cdot (1 - (\vec a \cdot \vec n)^2) & = N\_2^2 \cdot(1-(\vec b \cdot \vec n)^2) 
\end{cases}
$$

化解上式我们可以得到关于$k$的二次方程：

$$k^2 + 2(\vec a\cdot \vec n)k + (1-(\frac{N\_2}{N\_1})^2) = 0$$

求解二次方程可能会得到两个k值，根据折射定理，使得$\vec a\cdot \vec b$值更大的k值为所求的折射光线的系数，进而得到折射光线：

```javascript
refraction_ray = uniform_light + k * uniform_normal
```

### 计算镜面反射光
![镜面反射](../../images/mirror.png)

镜面反射光线计算可用向量计算简洁的得出，如上图中的入射光线A，反射光线B可以按如下计算：

$\vec B = \vec A + 2(\vec N - \vec A) = 2 \vec N - \vec A$

实际计算时，对于单位长度的入射光线$\vec a$和单位长度的折射光线$\vec n$，有

$\vec b = \vec a - 2(\vec a\cdot \vec n)\vec n$


# 参考文献
[jsrt](http://antirez.com/misc/rt.html)
[Fundamentals of Ray Tracing](http://www.cosinekitty.com/raytrace/contents.html)

# 未完待续


















[TOC]