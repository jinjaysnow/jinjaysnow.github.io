// js only creates and insert parts + click events adds classes

var numOfPieces = 6 * 6;

var frag = document.createDocumentFragment();

function insertInnerPieces($el, innerPieces) {
    for (var i = 0; i < innerPieces; i++) {
        var $inner = document.createElement('div');
        $inner.classList.add('popup__piece-inner');
        $el.appendChild($inner);
    }
};

for (var i = 1; i <= numOfPieces; i++) {
    var $piece = document.createElement('div');
    $piece.classList.add('popup__piece');

    insertInnerPieces($piece, 3);
    frag.appendChild($piece);
}

document.querySelector('.popup__pieces').appendChild(frag);

var $popupsCont = document.querySelector('.popups-cont');
var $popup = document.querySelector('.popup');
var popupAT = 900;

document.querySelector('.popup-btn').addEventListener('click', function() {
    resume();
    $popupsCont.classList.add('s--popup-active');
    $popup.classList.add('s--active');
});

function closeHandler() {
    stop();
    $popupsCont.classList.remove('s--popup-active');
    $popup.classList.remove('s--active');
    $popup.classList.add('s--closed');

    setTimeout(function() {
        $popup.classList.remove('s--closed');
    }, popupAT);
}

document.querySelector('.popup__close').addEventListener('click', closeHandler);

document.querySelector('.popups-cont__overlay').addEventListener('click', closeHandler);

/*********************Ray Tracing*********************/
var ctx; // 绘制context
var pixels; // 像素点
var screen_width = 900; // 宽
var screen_height = 600; // 高
var frame = 0; // 帧
var animate = 0; // 是否动画

var ssss = []; // 确定执行时间

// 初始化
function init() {
    ctx = document.getElementById('paper').getContext('2d');
    pixels = ctx.createImageData(screen_width, screen_height);
    for (var i = 0; i < pixels.data.length; i += 4) {
        pixels.data[i + 0] = 000;
        pixels.data[i + 1] = 000;
        pixels.data[i + 2] = 000;
        pixels.data[i + 3] = 255;
    }
    ctx.putImageData(pixels, 0, 0);
};
// 绘制
function draw() {
    computeScene(); // 旋转物体后重新计算场景
    // 通过frame更新动画过程
    frame++;
    if (frame == screen_width) {
        console.log(Math.max.apply(null, ssss));
        console.log(Math.min.apply(null, ssss));
    };
    if (animate && frame < screen_width) {
        setTimeout(draw, 5);
    };
};
// 暂停
function stop() {
    animate = 0;
}
// 恢复
function resume() {
    if (frame < screen_width) {
        animate = 1;
        setTimeout(draw, 1000);
    };
}

/* 向量类
 * 默认初始化为(0,0,0)
 * 
 */
function Vector(x, y, z) {
    if (arguments.length == 0) {
        x = y = z = 0;
    }
    this.x = x;
    this.y = y;
    this.z = z;
}
Vector.prototype = {
    // 设置x, y, z
    set: function(x, y, z) {
        this.x = x;
        this.y = y;
        this.z = z;
    },
    // 向量长度
    magnitude: function() {
        return Math.sqrt(this.x * this.x + this.y * this.y + this.z * this.z);
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
        return (this.x * v.x + this.y * v.y + this.z * v.z);
    },
    // 减法
    sub: function(v) {
        var r = new Vector(this.x - v.x, this.y - v.y, this.z - v.z);
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
        normalToPoint: function(x, y, z) {
            x -= this.center.x;
            y -= this.center.y;
            z -= this.center.z;
            // 归一化 
            x /= this.radius;
            y /= this.radius;
            z /= this.radius;
            var result = new Vector(x, y, z);
            return result;
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
            var xyz_dot = (x * x) + (y * y) + (z * z);
            var b = (x * ray.direction.x) + (y * ray.direction.y) + (z * ray.direction.z);
            var disc = b * b - xyz_dot + this.radius * this.radius;

            var type = 0;
            if (disc > 0) {
                var d = Math.sqrt(disc);
                var root1 = b - d;
                var root2 = b + d;
                if (root2 > 0) {
                    if (root1 < 0) {
                        if (root2 < distance) {
                            distance = root2;
                            type = -1;
                        }
                    } else {
                        if (root1 < distance) {
                            distance = root1;
                            type = 1;
                        }
                    }
                }
            }
            return { type: type, dist: distance };
        }
    }
    /* 平面
     * 三个点确定一个平面
     */
function Plane(x1, y1, z1, x2, y2, z2, x3, y3, z3) {
    /* 平面内部表示为:
     * ax + by + cz + d = 0
     * (a, b, c)为平面的法线
     */
    var v1x = x1 - x2,
        v1y = y1 - y2,
        v1z = z1 - z2;
    var v2x = x1 - x3,
        v2y = y1 - y3,
        v2z = z1 - z3;

    // 法线
    var nx = (v1y * v2z) - (v1z * v2y);
    var ny = (v1z * v2x) - (v1x * v2z);
    var nz = (v1x * v2y) - (v1y * v2x);

    // 代入一点坐标求解d
    this.normal = new Vector(nx, ny, nz);
    this.d = -(nx * x1 + ny * y1 + nz * z1);
}
Plane.prototype = {
    normalToPoint: function(x, y, z) {
        var n = new Vector(this.normal.x, this.normal.y, this.normal.z);
        n.normalize();
        return n;
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
            distance = -(ndoro + this.d) / ndotrd;
            // 只有距离为正值时才会相交
            if (distance > 0) type = 1;
        }
        return { type: type, dist: distance };
    }
};
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
        var v0 = data['vertices'][f[0]];
        var v1 = data['vertices'][f[1]];
        var v2 = data['vertices'][f[2]];
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
    else if (x < 0 && y >= 0)
        return 1;
    else if (x < 0 && y < 0)
        return 2;
    else
        return 3;
}
var signTable = [
    [0, 1, 2, -1],
    [-1, 0, 1, 2],
    [2, -1, 0, 1],
    [1, 2, -1, 0]
];

function transformMulTransform(t1, t2) {
    var result = [];
    for (var i = 0; i < 3; i++) {
        var t = [];
        t[0] = t1[i][0] * t2[0][0] + t1[i][1] * t2[1][0] + t1[i][2] * t2[2][0];
        t[1] = t1[i][0] * t2[0][1] + t1[i][1] * t2[1][1] + t1[i][2] * t2[2][1];
        t[2] = t1[i][0] * t2[0][2] + t1[i][1] * t2[1][2] + t1[i][2] * t2[2][2];
        result[i] = t;
    };
    return result;
};

function xyzMultTransform(xyz, transform) {
    var result = [];
    result[0] = xyz[0] * transform[0][0] + xyz[1] * transform[1][0] + xyz[2] * transform[2][0];
    result[1] = xyz[0] * transform[0][1] + xyz[1] * transform[1][1] + xyz[2] * transform[2][1];
    result[2] = xyz[0] * transform[0][2] + xyz[1] * transform[1][2] + xyz[2] * transform[2][2];
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
            var v0 = this.vertices[f[0]];
            var v1 = this.vertices[f[1]];
            var v2 = this.vertices[f[2]];
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
            var p_distance = Math.abs(x * p_n.x + y * p_n.y + z * p_n.z + p_d);
            if (distance > p_distance) {
                distance = p_distance;
                index = i;
            };
        };
        if (distance > 1e-6) {
            console.log(distance);
        };
        // 复制normal对象，放置更改normal初始值
        var n = this.faces_plane[index].normal;
        var normal = new Vector(n.x, n.y, n.z);
        normal.normalize();
        var v0 = this.vertices[this.faces[index][0]];
        var cv = new Vector(this.center[0] - v0[0],
            this.center[1] - v0[1],
            this.center[2] - v0[2]);
        if (normal.dot_product(cv) > 0) {
            normal.x = -normal.x;
            normal.y = -normal.y;
            normal.z = -normal.z;
        };
        return normal;
    },
    intersect: function(ray) {
        var type = 0;
        var distance = +Infinity;

        // 光线源点到中心的向量
        x = this.center[0] - ray.origin.x;
        y = this.center[1] - ray.origin.y;
        z = this.center[2] - ray.origin.z;

        var result = [];
        for (var i = 0; i <= this.faces_plane.length - 1; i++) {
            // 先看是否与每一个平面相交
            var p = this.faces_plane[i];
            result[i] = p.intersect(ray);
            if (result[i].type != 0) {
                // 检查是否在多边形内部，使用改进的弧长法
                var f = this.faces[i];
                distance = result[i].dist;
                // 与该平面的交点坐标
                var pp = [ray.origin.x + ray.direction.x * distance,
                         ray.origin.y + ray.direction.y * distance,
                         ray.origin.z + ray.direction.z * distance];

                // 三维点变为二维点坐标
                var n = p.normal;
                var discard = 0;
                if (Math.abs(n.x) < Math.abs(n.y)) {
                    discard = 1;
                };
                if (Math.abs(n.x) < Math.abs(n.z)) {
                    discard = 2;
                };
                if (discard != 0) {
                    if (Math.abs(n.y) > Math.abs(n.z)) {
                        discard = 1;
                    } else {
                        discard = 2;
                    }
                };
                var coord = [];
                for (var j = 0; j < f.length; j++) {
                    var iii = [0,1,2];
                    iii.splice(discard, 1);
                    var v = this.vertices[f[j]];
                    var deltax = v[iii[0]] - pp[iii[0]],
                        deltay = v[iii[1]] - pp[iii[1]];
                    coord[j] = [deltax, deltay];
                };
                coord[f.length] = coord[0]; // coord中存放的是移动坐标系后的顶点的坐标

                var n = 0;
                var on_line = false;

                for (var j = 1; j <= coord.length - 1; j++) {
                    // 获取点所在的象限
                    var g0 = getQuadrant(coord[j - 1][0], coord[j - 1][1]);
                    var g1 = getQuadrant(coord[j][0], coord[j][1]);
                    // 弧长增量
                    var addition = signTable[g0][g1];
                    if (addition == 2) {
                        var f = coord[j][1] * coord[j - 1][0] - coord[j][0] * coord[j - 1][1];
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
                if (!on_line && n == 0) {
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
        return { type: type, dist: distance};
    }
};
// 灯光
function Light() {
    this.type = "light";
    this.center = new Vector();
};
// 物体
function Solid(name, o) {
    this.name = name;
    this.o = o;
    this.color = { r: 1, g: 1, b: 1 };
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
    traceRay: function(ray, depth) {
        var obj = null;
        var color = { r: 0, g: 0, b: 0 };
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
            var x = ray.origin.x + ray.direction.x * distance,
                y = ray.origin.y + ray.direction.y * distance,
                z = ray.origin.z + ray.direction.z * distance;
            // 交点处的法线
            var normal = obj.o.normalToPoint(x, y, z);

            for (var j = 0; j < this.lights.length; j++) {
                var light = this.lights[j];
                // 计算光线到交点的向量
                var lx = light.o.center.x - x;
                var ly = light.o.center.y - y;
                var lz = light.o.center.z - z;
                // 归一化
                var len = Math.sqrt(lx * lx + ly * ly + lz * lz);
                if (len == 0) len = 1;
                lx /= len;
                ly /= len;
                lz /= len;
                // 阴影计算
                var pldistance = Math.sqrt(
                    (x - light.o.center.x) * (x - light.o.center.x) +
                    (y - light.o.center.y) * (y - light.o.center.y) +
                    (z - light.o.center.z) * (z - light.o.center.z));
                var sray = new Ray();

                sray.origin.set(x, y, z);
                // 增加一小点，避免光线与当前点相交
                sray.origin.x += lx / 10000;
                sray.origin.y += ly / 10000;
                sray.origin.z += lz / 10000;
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
                var cosine = normal.x * lx + normal.y * ly + normal.z * lz;
                if (cosine < 0) cosine = 0;
                // 简单的纹理，只对下方的平面有效
                if (obj.name == "Ground") {
                    var temp_x = Math.abs(Math.ceil(x)) % 2;
                    var temp_y = Math.abs(Math.ceil(z)) % 2;
                    if (temp_x == temp_y) {
                        obj.color.r = 1.0;
                        obj.color.g = 1.0;
                        obj.color.b = 1.0;
                    } else {
                        obj.color.r = 0.1;
                        obj.color.g = 0.1;
                        obj.color.b = 0.1;
                    };
                };
                color.r += cosine * obj.color.r * light.color.r;
                color.g += cosine * obj.color.g * light.color.g;
                color.b += cosine * obj.color.b * light.color.b;
                // 折射
                if (obj.specularity > 0) {
                    var vrx = lx - normal.x * cosine * 2,
                        vry = ly - normal.y * cosine * 2,
                        vrz = lz - normal.z * cosine * 2;
                    var cosSigma = (ray.direction.x * vrx) +
                        (ray.direction.y * vry) +
                        (ray.direction.z * vrz);
                    if (cosSigma > 0) {
                        var specularity = obj.specularity;
                        color.r += light.color.r * specularity * Math.pow(cosSigma, 64);
                        color.g += light.color.g * specularity * Math.pow(cosSigma, 64);
                        color.b += light.color.b * specularity * Math.pow(cosSigma, 64);
                    }
                }
                // 镜面反射
                if (obj.reflection > 0 && depth < 5) {
                    var rr = new Ray();
                    var dotnr = (ray.direction.x * normal.x) +
                        (ray.direction.y * normal.y) +
                        (ray.direction.z * normal.z);
                    rr.origin.set(x, y, z);
                    rr.direction.set(ray.direction.x - 2 * normal.x * dotnr,
                        ray.direction.y - 2 * normal.y * dotnr,
                        ray.direction.z - 2 * normal.z * dotnr);
                    rr.origin.x += rr.direction.x / 10000;
                    rr.origin.y += rr.direction.y / 10000;
                    rr.origin.z += rr.direction.z / 10000;
                    var rcolor = this.traceRay(rr, depth + 1);
                    color.r *= 1 - obj.reflection;
                    color.g *= 1 - obj.reflection;
                    color.b *= 1 - obj.reflection;
                    color.r += rcolor.color.r * obj.reflection;
                    color.g += rcolor.color.g * obj.reflection;
                    color.b += rcolor.color.b * obj.reflection;
                }
            }
            if (color.r > 1) color.r = 1;
            if (color.g > 1) color.g = 1;
            if (color.b > 1) color.b = 1;
        }
        return { obj: obj, color: color }
    },
    traceScene: function(camera) {
        var ray = new Ray();
        ray.origin = camera.position;
        var x = frame;
        if (x < screen_width) {
            for (var y = 0; y < screen_height; y++) {
                var direction = [(x - screen_width / 2) / 100,
                    -(y - screen_height / 2) / 100,
                    camera.focus
                ];
                direction = xyzMultTransform(direction, camera.transform);
                ray.direction.set(direction[0], direction[1], direction[2]);
                ray.direction.normalize();
                var trace = this.traceRay(ray, 0);
                var offset = x * 4 + y * 4 * screen_width;
                pixels.data[offset + 0] = trace.color.r * 255;
                pixels.data[offset + 1] = trace.color.g * 255;
                pixels.data[offset + 2] = trace.color.b * 255;
            }
            ctx.putImageData(pixels, 0, 0);
        };
    }
}

function Camera() {
    this.position = new Vector();
    this.transform = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ];
    this.focus = 4.0;
}

// 场景
var scene = new Scene();
var g_data = {
    'center': [0, 0, 0],
    'vertices': [
        [-1, -1, -1],
        [1, -1, -1],
        [1, -1, 1],
        [-1, -1, 1],
        [-1, 1, -1],
        [1, 1, -1],
        [1, 1, 1],
        [-1, 1, 1]
    ],
    'faces': [
        [0, 1, 2, 3],
        [0, 1, 5, 4],
        [1, 2, 6, 5],
        [4, 5, 6, 7],
        [0, 3, 7, 4],
        [2, 3, 7, 6]
    ],
};

var geometry = new Geometry(g_data);
var scale_t = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
];
geometry.transform = transformMulTransform(geometry.transform, scale_t);
geometry.makeTransform();
var gg = scene.addObject(new Solid("Geometry", geometry));
gg.color.r = 1.0;
gg.color.g = 0.3;
gg.color.b = 0.3;
gg.specularity = .5;
gg.reflection = .1;

var plane = scene.addObject(new Solid("Ground", new Plane(2, -1, 0, 0, -1, -4, 2, -1, 2)));

var light1 = scene.addLight(new Solid("Light 1", new Light()));
var light2 = scene.addLight(new Solid("Light 2", new Light()));
var light3 = scene.addLight(new Solid("Light 3", new Light()));

var camera = new Camera();

var sphere1 = scene.addObject(new Solid("Sphere 1", new Sphere()));
var sphere2 = scene.addObject(new Solid("Sphere 2", new Sphere()));
var sphere3 = scene.addObject(new Solid("Sphere 3", new Sphere()));
sphere3.o.radius = 1.0;
sphere3.o.center.z = 3;
sphere3.specularity = 1.0;
sphere3.reflection = 1.0;

sphere1.o.radius = 1.0;
sphere1.o.center.x = -3.0;

sphere2.o.center.x = 3.0;
sphere2.o.radius = 1;
light1.o.center.set(4, 8, -6);
light2.o.center.set(-6, 8, -6);
light3.o.center.set(6, 6, -6);
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
sphere1.color.g = 1;
sphere1.color.b = 0;
sphere1.specularity = 1.0;
sphere1.reflection = .0;
sphere2.color.r = 0.;
sphere2.color.g = 1;
sphere2.color.b = 0.;
sphere2.specularity = .5;
sphere2.reflection = .1;
plane.color.r = .3;
plane.color.g = .3;
plane.color.b = .3;

camera.position = new Vector(0, 0, -6);
camera.focus = 6.0;
var theta = 45 * Math.PI / 180.0;
camera.position.y = 6.0 * Math.sin(theta);
camera.position.z = -6.0 * Math.cos(theta);
camera.transform = makeRotateY(-45);

// 绕Y轴旋转矩阵
function makeRotateY(angle) {
    var sin_theta = Math.sin(angle / 180.0 * Math.PI);
    var cos_theta = Math.cos(angle / 180.0 * Math.PI);
    return [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, cos_theta, -sin_theta, 0.0],
        [0.0, sin_theta, cos_theta, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ];
}
// 动画过程
function computeScene() {
    var st = new Date().getTime();
    scene.traceScene(camera);
    var st2 = new Date().getTime() - st;
    ssss.push(st2);
}
window.onload = function() { init(); };