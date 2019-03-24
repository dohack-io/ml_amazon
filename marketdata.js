var json = require('./data.json');
arrsin = []
arrsout= []
n=1;
for(var g =0;g<n;g++){
arr = json.products[0].csv[g];
i=0;
k=0;
boxlength = 24*60*60/2;
maximum = timeSinceRec(toSec(arr[arr.length-2]));
current = boxlength;
means=[];
while(current <= maximum){
    days=[]
    j=0;
    while(timeSinceRec(toSec(arr[i]))<current){
        if(arr[i+1]>0){
            days[j]=arr[i+1];
            j++;
        }
        i+=2
    }
    means[k] = sum(days)/j;
    k++;
    current+=boxlength;
}
means = clean(means);
act = means;
//console.log(act);
means = normalize(means);
for(var i=0;i<means.length;i++){
    console.log(means[i],i/2);
}
sub = subsets(means,120,1,2);
arrsin[g] = sub[0];
arrsout[g] = sub[1];

}
dict = {inputs:conc(arrsin),outputs:conc(arrsout),actual:act}
var dictstring = JSON.stringify(dict);
var fs = require('fs');
fs.writeFile("train.json", dictstring);
//console.log(means)



function timeSinceRec(i){
    return i-toSec(arr[0])
}
function toSec(n){
    return (n+21564000)*60
}
function sum(array){
    count=0
    for(var i=0;i<array.length;i++){
        count+=array[i];
    }
    return count;
}
function clean(array){
    c = [];
    b=0;
    while(array[b]<0 || isNaN(array[b])){
        b++;
    }
    for(var i=0;i<array.length;i++){
        if(array[i+b]>=0){
            c[i]=array[i+b];
        }else{
            c[i]=c[i-1];
        }
    }
    return c;
}

function normalize(array){
    c = [[1]];
    last = array[0];
    for(var i=1;i<array.length;i++){
        c[i]=[array[i]/last];
        last=array[i];
    }
    return c;
}
function subsets(array,input,output,step){
    cur=0;
    i=0;
    len=input+output;
    setsin=[];
    setsout=[];
    while(cur<array.length-len){
        setsin[i]=array.slice(cur,cur+input);
        setsout[i]=array.slice(cur+input,cur+len);
        cur+=step;
        i++;
    }
    return [setsin,setsout];
}
function conc(array){
    res = []
    for(var i=0;i<n;i++){
        res = res.concat(array[i]);
    }
    //console.log(res);
    return res;
}


