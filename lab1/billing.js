
var stream = require('fs').createReadStream('data.csv');
var lineReader = require('readline').createInterface({
    input: stream
});

var lineIndex = -1;
lineReader.on('line', function (line) {
    lineIndex++;
    if (lineIndex == 0) {
        return;
    }
    traficate(line)
});

stream.on("end", function() {
    printResult()
})

var fullDurationg = 0;
var fullSmsCount = 0;

function traficate(line) {
    var [time, origin, dst, duration, smsCount] = line.split(",");
    duration = parseFloat(duration);
    smsCount = parseFloat(smsCount);

    if (origin == "933156729") {
        fullDurationg += duration;
        fullSmsCount += smsCount;
    }
}

function printResult() {
    fullDurationg = fullDurationg < 20 ? 0 : fullDurationg - 20
    
    billCall = fullDurationg * 2;
    billSms = fullSmsCount * 2

    console.log("Calls: " + billCall)
    console.log("Sms: " + billSms)
    console.log("Total: " + (billCall + billSms))
}