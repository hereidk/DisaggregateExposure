var doctitle=new String(document.title);
var urlhref=new String(location.href);
var lastmod=new Date(document.lastModified);
var year=lastmod.getYear(document.lastModified);

var metaElements = new Array();
metaElements = document.getElementsByTagName ('META');
for (var m = 0; m < metaElements.length; m++)
	switch(metaElements[m].name)
	{
	case 'operator':
		var operator = metaElements[m].content;
		break;
	case 'questions':
		var questions = metaElements[m].content;
		break;
	case 'return':
		var breadcrumb = metaElements[m].content;
		break;
	case 'topic':
		var topic = metaElements[m].content;
		break;
	}
document.write("<table border=\"0\"  width=\"100%\" summary=\"layout table\"><tbody><tr>");
document.write("<td align=\"left\"><div class=\"smallestblue\"> <a href=\"http://www.noaa.gov/\" title=\"National Oceanic and Atmospheric Administration\">NOAA</a> &gt; <a href=\"http://www.nesdis.noaa.gov/\" title=\"NOAA Satellite and Information Service\">NESDIS</a> &gt; <a href=\"//www.ngdc.noaa.gov/ngdc.html\" title=\"Natonal Geophysical Data Center\">NGDC</a>");
switch(breadcrumb)
{
case "gnssw":
        document.write(" &gt; <a href=\"//www.ngdc.noaa.gov/stp/gnssw2007/index.html\">NOAA GNSS Workshop</a>");
        break;
case "class":
	document.write(" &gt; <a href=\"//www.ngdc.noaa.gov/dmsp/class_workshop/class.html\">CLASS Users&#039; Workshop</a>");
	break;
case "geomag":
	document.write(" &gt; <a href=\"//www.ngdc.noaa.gov/mggd.html\">MGGD</a>&amp;<a href=\"/stp/stp.html\">STP</a> &gt; <a href=\"//www.ngdc.noaa.gov/geomag/geomag.shtml\">Geomagnetism</a>");
	break;
case "hazard":
	document.write(" &gt; <a href=\"//www.ngdc.noaa.gov/mggd.html\">MGGD</a> &gt; <a href=\"//www.ngdc.noaa.gov/hazard/\">Natural Hazards</a>");
	break;
case "hazards":
	document.write(" &gt; <a href=\"//www.ngdc.noaa.gov/mggd.html\">MGGD</a> &gt; <a href=\"//www.ngdc.noaa.gov/hazard/\">Natural Hazards</a>");
	break;
case "maps":
	document.write(" &gt; <a href=\"//www.ngdc.noaa.gov/maps/\">Interactive Maps</a>");
	break;
case "mgg":
	document.write(" &gt; <a href=\"//www.ngdc.noaa.gov/mggd.html\">MGGD</a> &gt; <a href=\"//www.ngdc.noaa.gov/mgg/mggd.html\">Marine Geology &amp; Geophysics</a>");
	break;
case "hydro":
	document.write(" &gt; <a href=\"//www.ngdc.noaa.gov/mggd.html\">MGGD</a> &gt; <a href=\"//www.ngdc.noaa.gov/mgg/bathymetry/hydro.html\">NOS Hydro Data</a>");
	break;
case "bathy":
	document.write(" &gt; <a href=\"//www.ngdc.noaa.gov/mggd.html\">MGGD</a> &gt; <a href=\"//www.ngdc.noaa.gov/mgg/mggd.html\">Marine Geology &amp; Geophysics</a> &gt; <a href=\"/mgg/bathymetry/relief.html\">Bathymetry &amp; Relief</a>");
	break;
case "space":
	document.write(" &gt; <a href=\"//www.ngdc.noaa.gov/stp/stp.html\">STP</a> &gt; <a href=\"//www.ngdc.noaa.gov/stp/spaceweather.html\">Space Weather</a>");
	break;
case "stp":
	document.write(" &gt; <a href=\"//www.ngdc.noaa.gov/stp/stp.html\">Solar - Terrestrial Physics</a>");
	break;
case "dmsp":
	document.write(" &gt; <a href=\"//www.ngdc.noaa.gov/dmsp/\">Earth Observation</a>");
	break;
case "eog":
	document.write(" &gt; <a href=\"//www.ngdc.noaa.gov/dmsp/\">Earth Observation</a>");
	break;
}
document.write("</div></td>");
document.write("<td align=\"right\"><div class=\"smallestblue\">");
if (topic == null)
document.write("Questions: <a href=\"mailto:" + questions + "@noaa.gov?subject=RE: " + urlhref + "\" title=\"ask questions about data on this Web page\">" + questions + "@noaa.gov</a>");
else
{document.write("Questions: <a href=\"mailto:" + questions + "@noaa.gov?subject=" + topic + "\" title=\"ask questions about data on this Web page\">" + questions + "@noaa.gov</a>");
}
document.write("</div></td></tr><tr><td colspan=\"2\"><hr class=\"smallestblue\" size=\"1\" noshade></td></tr></tbody></table><div align=\"center\" class=\"footltbg\">");
document.write("<a href=\"//www.ngdc.noaa.gov/ngdc.html\" title=\"go to NGDC home\">NGDC Home</a> | ");
document.write("<a href=\"//www.ngdc.noaa.gov/ngdcinfo/phone.html\" class=\"footltbg\" title=\"go to NGDC directory of contacts\">Contacts</a> | ");
document.write("<a href=\"//www.ngdc.noaa.gov/ngdcinfo/onlineaccess.html\" class=\"footltbg\" title=\"go to data available from NGDC\">Data</a> | ");
document.write("<a href=\"//www.ngdc.noaa.gov/ngdcinfo/privacy.html#disclaimer\" class=\"footltbg\" title=\"go to NGDC privacy, disclaimer, and copyright notices\">Disclaimers</a> | ");
document.write("<a href=\"//www.ngdc.noaa.gov/education/education.html\" class=\"footltbg\" title=\"go to education and outreach resources and links\">Education</a> | ");
document.write("<a href=\"//www.ngdc.noaa.gov/products/ngdc_news.html\" class=\"footltbg\" title=\"go to NGDC news and features\">News</a> | ");
document.write("<a href=\"//www.ngdc.noaa.gov/ngdcinfo/privacy.html\" class=\"footltbg\" title=\"go to NGDC privacy, disclaimer, and copyright notices\">Privacy Policy</a> | ");
document.write("<a href=\"//www.ngdc.noaa.gov/sitemap/sitemap.html\" class=\"footltbg\" title=\"go to an index of the NGDC Web site\">Site Map</a> | ");
document.write("<a href=\"//www.ngdc.noaa.gov/feedback/\" class=\"footltbg\" title=\"provide feedback on the NGDC Web site\">Take Our Survey</a><br /><br />");
document.write("</div><br />");
document.write("<script type=\"text/javascript\">if (window.parent == window) {var _gaq = _gaq || [];_gaq.push(['_setAccount', 'UA-44375312-1']);_gaq.push(['_setDomainName', 'www.ngdc.noaa.gov']);_gaq.push(['_setAllowLinker', true]);_gaq.push(['_trackPageview']);(function() {var ga = document.createElement('script'); ga.type = 'text/javascript';ga.async = true;ga.anonymizeIp = true;ga.src = ('https:' == document.location.protocol \? 'https://ssl' : 'http://www') \+ '.google-analytics.com/ga.js';var s = document.getElementsByTagName('script')[0];s.parentNode.insertBefore(ga, s);})();}</script><br />");
