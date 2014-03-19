package com.meilishuo.util;

import java.io.File;
import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.LineIterator;

public class NginxLogUtil {

	private static final int REQUEST_METHOD_INDEX = 0;
	private static final int REQUEST_BODY_INDEX = 1;
	private static final int REQUEST_HTTP_VERSION_INDEX = 2;

	private boolean flag = false;
	private String[] tokens;
	private String[] requestTokens = null;
	private Map<String, String> cookie = null;

	public void debug(boolean debug) {
		flag = debug;
	}

	private boolean isEmpyt(String token) {
		return token.trim().length() == 0 || token == null ? true : false;
	}

	public int split(String line) {
		if (line == null || line.trim().length() == 0) {
			return 0;
		}

		String[] source = line.split("]");
		tokens = new String[source.length];

		for (int index = 0; index < source.length; index++) {
			String token = source[index].trim();
			if (token.startsWith("["))
				token = token.substring(1);
			tokens[index] = token;
			System.out.println(token);
		}

		return tokens.length;
	}

	public String getVisitIp() {
		return tokens[0];
	}

	public String getRemoteUser() {
		return tokens[1];
	}

	public String getVisitTime(String targetDateFormat) {
		String logDateString = tokens[2] + " " + tokens[3];
		if (isEmpyt(targetDateFormat))
			return logDateString;

		if (flag)
			System.out.println("log date string : " + logDateString);

		SimpleDateFormat sourceFormat = new SimpleDateFormat(
				"dd/MMM/yyyy:HH:mm:ss", Locale.ENGLISH);
		SimpleDateFormat targetFormat = new SimpleDateFormat(targetDateFormat);
		Date targetDate = null;
		try {
			targetDate = sourceFormat.parse(logDateString);
		} catch (ParseException e) {
			System.out.println("Log Date Parser Failed ! ");
			return "";
		}
		String targetDateString;
		try {
			targetDateString = targetFormat.format(targetDate);
		} catch (Exception e) {
			System.out.println("target Date Format maybe unParserable !");
			targetDateString = "";
		}

		return targetDateString;
	}

	public String getRequest() {
		if (!isEmpyt(tokens[3])) {
			return tokens[3];
		} else {
			return null;
		}
	}

	private boolean checkRequestToken() {
		if (requestTokens == null || requestTokens.length != 3) {
			return false;
		} else {
			return true;
		}
	}

	private String[] splitBySpace(String line) {
		if (isEmpyt(line)) {
			return null;
		} else {
			return line.split(" ");
		}
	}

	private void checkAndSplit() {
		if (!checkRequestToken()) {
			this.tokens = splitBySpace(tokens[3]);
		}
	}

	public String getRequestMethod() {
		checkAndSplit();
		return requestTokens[REQUEST_METHOD_INDEX];
	}

	public String getRequestBody() {
		checkAndSplit();
		return requestTokens[REQUEST_BODY_INDEX];
	}

	public String getRequestHTTPVersion() {
		checkAndSplit();
		return requestTokens[REQUEST_HTTP_VERSION_INDEX];
	}

	public String getStatus() {
		return tokens[4];
	}

	public String getBodyBytesSent() {
		return tokens[5];
	}

	public String getRefer() {
		return tokens[6];
	}

	public String getUserAgent() {
		return tokens[7];
	}

	public String getHttpXForwardedFor() {
		return tokens[8];
	}

	public String getCookie() {
		return tokens[9];
	}

	public Map<String, String> getCookieMap() {
		Map<String, String> map = new HashMap<String, String>();
		if (flag)
			System.out.println("Cookie : " + tokens[9]);

		String[] array = tokens[9].split("; ");
		for (String token : array) {
			String[] pair = token.split("=");
			if (pair.length != 2) {
				System.out.println(token + " parser failed");
				continue;
			}
			map.put(pair[0], pair[1]);
		}

		cookie = map;
		return map;
	}

	public String getCookieVal(String cookieKey) {
		if (cookie == null) {
			getCookieMap();
		}

		if (cookie.containsKey(cookieKey)) {
			return cookie.get(cookieKey);
		} else {
			return null;
		}
	}

	public String getMLSGloablKey() {
		if (cookie == null) {
			getCookieMap();
		}

		if (cookie.keySet().contains("MEILISHUO_GLOBAL_KEY")) {
			return cookie.get("MEILISHUO_GLOBAL_KEY");
		} else {
			return null;
		}
	}

	public String getRequestTime() {
		return tokens[10];
	}

	public String getUpStreamAddr() {
		return tokens[11];
	}

	public String getUpStreamResponseTime() {
		return tokens[12];
	}

	public String getSeaShell() {
		String[] array = tokens[13].split("=");
		if (array.length != 2)
			return null;

		return array[1];
	}

	public String getPostData() {
		return tokens[14];
	}

	public String getNginxTime() {
		return tokens[15];
	}

	public String humanReadableNginxTime(String targetFormat) {
		if (isEmpyt(targetFormat)) {
			throw new IllegalArgumentException("target format is empty");
		}

		long timestamp = (long) (Double.valueOf(tokens[15]) * 1000);
		SimpleDateFormat format = new SimpleDateFormat(targetFormat);
		String date = format.format(new Date(timestamp));
		return date;
	}

	public static void main(String[] args) throws IOException {
		final String target_format = "yyyy-MM-dd HH:mm:ss";
		LineIterator iterator = FileUtils.lineIterator(new File("nginx.log"));
		// while (iterator.hasNext())
		{
			String line = iterator.nextLine();
			NginxLogUtil util = new NginxLogUtil();
			int length = util.split(line);
			System.out.println(length);
			// for (String string : target)
			// System.out.println(string);

			System.out.println("visit ip    : " + util.getVisitIp());
			System.out.println("remote user : " + util.getRemoteUser());
			System.out.println("visit time  : "
					+ util.getVisitTime(target_format));

			System.out.println("request : " + util.getRequest());
			System.out.println("request Method : \t ");
			System.out.println("request Method : \t ");
			System.out.println("request Method : \t ");
			/*
			 * '','','','','','','','','','','','',''
			 */

			System.out.println("status : " + util.getStatus());
			System.out.println("body_bytes_sent : " + util.getBodyBytesSent());
			System.out.println("refer : " + util.getRefer());
			System.out.println("user_agent : " + util.getUserAgent());
			System.out.println("http_x_forwarded_for : "
					+ util.getHttpXForwardedFor());
			System.out.println("cookie : " + util.getCookie());
			System.out.println("request_time : " + util.getRequestTime());
			System.out.println("upstream_addr : " + util.getUpStreamAddr());
			System.out.println("upstream_response_time : "
					+ util.getUpStreamResponseTime());
			System.out.println("seashell : " + util.getSeaShell());
			System.out.println("post_data : " + util.getPostData());
			System.out.println("nginx_time : " + util.getNginxTime());
			System.out.println("readable nginx time : "
					+ util.humanReadableNginxTime("yyyy-MM-dd:HH:mm:ss"));

			for (String key : util.getCookieMap().keySet()) {
				System.out.println(String.format("Cookie Pair %s --> %s", key,
						util.getCookieVal(key)));
			}
		}

		iterator.close();
	}
}
