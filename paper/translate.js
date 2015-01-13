// 获取元素子元素
var getChildNodes=function(ele){
   var childArr=ele.children || ele.childNodes,
        childArrTem=new Array();  //  临时数组，用来存储符合条件的节点
    for(var i=0,len=childArr.length;i<len;i++){
        if(childArr[i].nodeType==1){
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
	// 子元素节点集合
	enChildNodes = getChildNodes(en_div);
	zhChildNodes = getChildNodes(zh_div);

	for (var i = 1; i <= enChildNodes.length - 1; i++) {

		var mTop = enChildNodes[i].offsetTop - enChildNodes[i-1].offsetTop - zhChildNodes[i-1].offsetHeight;
		zhChildNodes[i].style.marginTop = String(mTop + "px");
	};
}

updatePos();
window.onload = function(){updatePos();};
