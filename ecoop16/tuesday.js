$(document).ready(function(){
	var colWidth = '175px' // 169 best A4 fit
		
	// do the dirty naughty stuff first
	$('#header-curryon').text('Curry On')
	$('.session-end-text').text("Session end")
	$('#empty-7').css({'height' : '6px'}) // 10 minutes
	$('#empty-1').css({'border-right' : 'solid 1px black'})

	// adjust borders (skip for cell 1:1) and column width for the table
	$('.table-elem').css('layout', 'fixed')

	$('tr')[0].remove()
	$('.table-session').each(function(index, obj) {
		if ($(obj).parent('td[colspan]').not('[colspan=1]').length > 0) {
			$(obj).css('width', "100%")
		} else {
			$(obj).css('width', colWidth)
		}
	})
	$($('tr')[0]).find('td').each(function(index, obj) {
		if (index > 0) $(obj).css('width', colWidth)
	})
	$('.table-elem').css({'border-left' : 'none', 'border-top' : 'none'})	
	$($('tr')[0]).find('td').each(function(index, obj) {
		if (index > 0) {
			if (index == 1) {
				$(obj).css('border-left', 'solid 2px')
			}
			$(obj).css({'border-top' : 'solid 2px', 'border-color' : 'black'})
		}
	})
	var timeSlots = $('td.td-time')
	timeSlots.each(function(key, obj) {
		var startHour = $(obj).text().substring(0,5)
		if (key == timeSlots.length - 1) {
			var endHour = $(obj).text().substring(6,11)
			$(obj).css("position", "relative")
			$(obj).html(startHour+"<div style=\"position: absolute; bottom: 0\">"+endHour+"</div>")
		} else {
			$(obj).html(startHour)
		}
		$(obj).css({'border-left' : 'solid 2px'})
	})
	
	// define tracks & colors
	var eventColors = new Array();
	eventColors['curryon'] = 'orange'; // yellow
	eventColors['ftfjp'] = 'blue';
	eventColors['cop'] = 'green';
	eventColors['grace'] = 'yellow';
	eventColors['jstools'] = 'magenta';
	var receptionColor = 'purple'
	
	// assign colors to cells
	$('.header-track').css('background-color', miscColors['event'])
	$('.td-catering').css('background-color', miscColors['event'])
	$('.td-catering-level').css('background-color', miscColors['event'])
	$('.empty-td').css('background-color', miscColors['event'])
	
	// alternate colors for time markers and set valign
	$('td.td-time').each(function(index, obj){
		if (index % 2 == 0) {
			$(obj).css('background-color', miscColors['timeSlotEven'])
		} else {
			$(obj).css('background-color', miscColors['timeSlotOdd'])
		}
		$(obj).css('vertical-align', 'top')
	});
	
	// track-specific transformations
	for (var key in eventColors) {
		// set background color for non-header cells
		$('.td-'+key+':not(.header-track)').css('background-color', lightColors[eventColors[key]])
		
		// format event titles
		$('#header-'+key).css({'color' : darkColors[eventColors[key]], 'font-weight' : 'bold', 'font-family' : 'Impact', 'font-size' : '133%'})
		
		// set session titles with darker background
		$('.td-'+key+' .session-title').css({'color' : 'white', 'font-weight' : 'bold', 'background-color' : darkColors[eventColors[key]], 'font-family' : 'Helvetica', 'font-size' : '90%'})
		
		$('.td-'+key+'.td-session').each(function(index, obj) {
			$(obj).find('.session-slot-time').css({'background-color' : mediumColors[eventColors[key]], 'font-weight' : 'bold', 'font-size' : '90%'})
			$(obj).find('.session-slot-author').css({'background-color' : mediumColors[eventColors[key]], 'font-weight' : 'bold', 'font-size' : '90%'})
			$(obj).find('.session-end-time').css({'background-color' : mediumColors[eventColors[key]], 'font-weight' : 'bold', 'font-size' : '90%'})
			$(obj).find('.session-end-text').css({'background-color' : mediumColors[eventColors[key]], 'font-weight' : 'bold', 'font-size' : '90%'})
		});
		
	}
	
	// special colors for poster & workshop reception
	$('#catering-session-4').css('background-color', lightColors[receptionColor])
	$('#catering-session-4 .session-title').css({'color' : 'white', 'font-weight' : 'bold', 'background-color' : darkColors[receptionColor], 'font-family' : 'Helvetica', 'font-size' : '90%'})
	$('#catering-session-4 .session-slot-time').css({'background-color' : mediumColors[receptionColor], 'font-weight' : 'bold', 'font-size' : '90%'})
	$('#catering-session-4 .session-slot-author').css({'background-color' : mediumColors[receptionColor], 'font-weight' : 'bold', 'font-size' : '90%'})
	$('#catering-session-4 .session-end-time').css({'background-color' : mediumColors[receptionColor], 'font-weight' : 'bold', 'font-size' : '90%'})
	$('#catering-session-4 .session-end-text').css({'background-color' : mediumColors[receptionColor], 'font-weight' : 'bold', 'font-size' : '90%'})
	
	// show room as part of the session title
	$('.table-session').each(function(index, obj) {
		var titleObj = $(obj).find('.session-title')
		var roomObj = $(obj).find('.session-room')
		//$(titleObj).html($(titleObj).text()+' <i>('+roomObj.text()+')</i>')
		$(titleObj).html($(titleObj).text()+' ('+roomObj.text()+')')
		$(roomObj).css('display', 'none')
	});
	
	// font families (some cool fonts: Big Caslon, Baskerville, Gill Sans - also Garamond but has issues with Chrome)
	$('th.td-day').css({'font-family' : 'Big Caslon'})
	$('.session-slot-title').css({'font-family' : 'Baskerville', 'font-style' : 'italic'}) // Gill Sans
	$('.session-slot-time').css({'font-family' : 'Baskerville'}) 
	$('.session-slot-author').css({'font-family' : 'Baskerville'})
	$('.session-end-time').css({'font-family' : 'Baskerville'})
	$('.session-time-text').css({'font-family' : 'Baskerville'})
	$('.td-catering').css({'font-family' : 'Baskerville'})
	$('td.td-time').css({'font-family' : 'Baskerville', 'font-weight' : 'bold', 'font-size' : '90%'})

	// text alignment and style
	$('td.td-catering').css('text-align', 'center')	
	$('td.session-room').css('font-style', 'italic')
	$('.td-session').css('vertical-align', 'top')
	$('table.table-session').css('layout', 'fixed')
	$('.session-slot-time').css({'width' : '50px', 'vertical-align' : 'top'})
	
	// padding and fixed heights
	$('.session-slot-time').css({'padding-top' : '4px'})
	$('.session-slot-author').css({'padding-top' : '4px'})
	$('.session-end-time').css({'padding-top' : '4px'})
	$('.session-end-text').css({'padding-top' : '4px'})
	$('td.td-time').css({'padding-left' : '4px', 'padding-right' : '4px'})
	$('.td-catering').css({'height' : '40px'})
	
	// add extra space for Session 7a & 7b
	//$('#curryon-session-8').height(function (index, height) { return (height + 6); });
}) 