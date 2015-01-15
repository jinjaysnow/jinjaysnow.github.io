// 获取元素子元素
var getChildNodes = function(ele){
    var childArr = ele.children || ele.childNodes,
    childArrTem = new Array();  //  临时数组，用来存储符合条件的节点
    for(var i = 0, len = childArr.length; i < len; i++){
        if(childArr[i].nodeType == 1){
            childArrTem.push(childArr[i]);
        }
    }
    return childArrTem;
}

// 将中文与英文的位置进行更新，函数需要在文档加载完成后进行
function updatePos () {
	// 获取英文与中文文档元素
	var en_div = document.getElementById("en");
	var zh_div = document.getElementById("zh");
	// 子元素节点 集合
	enChildNodes = getChildNodes(en_div);
	zhChildNodes = getChildNodes(zh_div);

	for (var i = 1; i <= enChildNodes.length - 1; i++) {
		var mTop = enChildNodes[i].offsetTop - enChildNodes[i-1].offsetTop - zhChildNodes[i-1].offsetHeight;
		zhChildNodes[i].style.marginTop = String(mTop + "px");
	};
}

// 文档加载结束进行一次界面布局
updatePos();
window.onload(function(){
	updatePos();
});
// 在MathJax加载完成后再次进行界面的布局
MathJax.Hub.Queue(function () {
	updatePos();
});

// 鼠标选中时高亮
$("span").mouseover(function(){
	var zhFirst = $("#zh")[0].firstchild;
	var enFirst = $("#en")[0].firstchild;
	// 只有两级查找时
	try{
		if($(this).parent().index(zhFirst | enFirst) != -1){
			var pos = $(this).parent().index(zhFirst | enFirst);
			var first = enChildNodes[pos].firstchild;
			var leftNode = getChildNodes(enChildNodes[pos]);
			var rightNode = getChildNodes(zhChildNodes[pos]);
			pos = $(this).index(first);
			leftNode[pos].classList.add("focus");
			rightNode[pos].classList.add("focus");
		}
	}catch(exception){
		// 三级查找
		if ($(this).parent().parent().index(zhFirst | enFirst) != -1) {
			// 第一级
			var pos = $(this).parent().parent().index(zhFirst | enFirst);
			var left = enChildNodes[pos];
			var right = zhChildNodes[pos];
			// 第二级
			pos = $(this).parent().index(left.firstchild);
			var left2 = getChildNodes(left)[pos];
			var right2 = getChildNodes(right)[pos];
			// 第三级
			pos = $(this).index(left2.firstchild);
			var left3 = getChildNodes(left2);
			var right3 = getChildNodes(right2);
			left3[pos].classList.add("focus");
			right3[pos].classList.add("focus");
		};
	}
});
$("span").mouseleave(function(){
	var zhFirst = $("#zh")[0].firstchild;
	var enFirst = $("#en")[0].firstchild;
	// 只有两级查找时
	try{
		if($(this).parent().index(zhFirst | enFirst) != -1){
			var pos = $(this).parent().index(zhFirst | enFirst);
			var first = enChildNodes[pos].firstchild;
			var leftNode = getChildNodes(enChildNodes[pos]);
			var rightNode = getChildNodes(zhChildNodes[pos]);
			pos = $(this).index(first);
			leftNode[pos].classList.remove("focus");
			rightNode[pos].classList.remove("focus");
		}
	}catch(exception){
		// 三级查找
		if ($(this).parent().parent().index(zhFirst | enFirst) != -1) {
			// 第一级
			var pos = $(this).parent().parent().index(zhFirst | enFirst);
			var left = enChildNodes[pos];
			var right = zhChildNodes[pos];
			// 第二级
			pos = $(this).parent().index(left.firstchild);
			var left2 = getChildNodes(left)[pos];
			var right2 = getChildNodes(right)[pos];
			// 第三级
			pos = $(this).index(left2.firstchild);
			var left3 = getChildNodes(left2);
			var right3 = getChildNodes(right2);
			left3[pos].classList.remove("focus");
			right3[pos].classList.remove("focus");
		};
	}
});
