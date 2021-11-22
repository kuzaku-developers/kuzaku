let isSwitcherEnabled = false;
let mouseDown = false;
let cachedPos = 0;

$(function() {
    $('#switcher-wrapper').click(function() {

        switchSwitcher();
    });

    $('#slide-bar').click(function(e) {
        moveSlider(e);
    });

    $(document).mousemove(function(e) {
        if(mouseDown) {
            moveSlider(e);
        }
    });

    $('#slide-bar').mousedown(function(e) {
        mouseDown = true;
    });

    $('#slide-bar').mouseup(function(e) {
        mouseDown = false;
    });

    $(document).mouseup(function() {
        mouseDown = false;
    });





   

});

function moveSlider(e, anim = true) {
    $('#slide-bar-circle').css('transition', 'none');

    let x = e.pageX - $('#slide-bar').position().left;
    let r = $('#slide-bar-circle').width() / 2;

    cachedPos = x;

    x -= r;

    if(x >= 0 && x <= $('#slide-bar').width() - 2 * r) {
        if(anim) {
            $('#slide-bar-circle').css('transition', 'transform 0.3s')
        }

        $('#slide-bar-circle').css('transform', 'translate(' + x + 'px)')
        $("body").get(0).style.setProperty("--slide-val", (x + r) + 'px');

        $('#value-translator').text(getSliderValue(140) + 'xp');
    }
}
function switchSwitcher() {
    let wrapperWidth = $('#switcher-wrapper').width();
    let circleD = $('#switcher-circle').width();

    $('#switcher-circle').css("transform", `translate(${isSwitcherEnabled ? 0 : wrapperWidth -  circleD}px, 0px)`);
    $('#switcher-wrapper').css("background", `${isSwitcherEnabled ? 'var(--brand-dark)' : 'var(--flat-green)'}`);


    isSwitcherEnabled = !isSwitcherEnabled;
}
function getSliderValue(max) {
    let x = cachedPos - 0.1 * cachedPos;
    let maximus = $('#slide-bar').width() - $('#slide-bar-circle').width();

    let res = (x * max) / maximus;

    return Math.round(res);
}

function levelingSystemEnabled() {
    return isSwitcherEnabled;
}
function setValue(val, maxi) {
    let translated = ($('#slide-bar').width() * val) / maxi;


    moveSlider({
        pageX: translated
    });
}
function loadall(ecoenabled, xppermsg) {
    console.log(xppermsg)
    if (ecoenabled=="true")
    {
        switchSwitcher()
        console.log(isSwitcherEnabled)
    }
    setValue(xppermsg, 140)
}