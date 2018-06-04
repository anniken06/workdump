package playground;

import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;

enum EXTENSION_CONSTANTS {
	RETURN_VALUE
}

public class Extensions {

	public static Map<String, Function<HashMap<String, Object>, HashMap<String, Object>>> extensionMap = new HashMap<String, Function<HashMap<String, Object>, HashMap<String, Object>>>();

	public static void setClassMethod(String methodName, Function method) {
		extensionMap.put(methodName, method);
	}

	public static Function getClassMethod(String methodName) {
		return extensionMap.get(methodName);
	}

	public static void displayAllExtensions() {
		extensionMap.forEach((key, value) -> System.out.println(key));
	}

	public static HashMap<String, Object> castMap(Object obj) {
		return (HashMap<String, Object>) obj;
	}

	public static void runTest() {
		String newMethodName = String.class.getName() + ".concatMaster3000";

		Extensions.setClassMethod(newMethodName, (kwargs) -> {
			HashMap<String, Object> args = castMap(kwargs);
			HashMap<String, Object> kwreturn = new HashMap<String, Object>();

			String concatted = "";
			for (Map.Entry<String, Object> entry : args.entrySet()) {
				concatted += entry.getKey() + ": " + String.valueOf(entry.getValue());
			}

			kwreturn.put(EXTENSION_CONSTANTS.RETURN_VALUE.toString(), "\"" + concatted + "\"");
			return kwreturn;
		});

		Object eval = Extensions.getClassMethod(newMethodName).apply(new HashMap<String, Object>() {
			{
				put("test1", 123);
				put("test2", true);
			}
		});

		System.out.println(newMethodName + "\'s result: " + eval);
		System.out.println(castMap(eval).get(EXTENSION_CONSTANTS.RETURN_VALUE.toString()));
		Extensions.displayAllExtensions();
	}
}
