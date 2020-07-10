var a = [];
// 声明变量let 和 var 返回的结果不同
for (let i = 0; i < 10; i++){
    a[i] = function () {
        console.log(i);
    };
}
a[6]()
// i 和 i 不在同一个作用域 python是在同一个作用域
for (let i = 0; i < 3; i++) {
  let i = 'abc';
  console.log(i);
}