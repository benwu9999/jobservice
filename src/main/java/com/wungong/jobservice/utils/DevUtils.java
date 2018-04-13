package com.wungong.jobservice.utils;

import java.io.IOException;

import org.codehaus.jackson.schema.JsonSchema;

import com.wungong.jobservice.model.Address;

public class DevUtils {

	public static void main(String[] args) throws Exception {
		System.out.println(getJsonSchema(Address.class));
	}
	
	private static String getJsonSchema(Class clazz) throws IOException {
	    org.codehaus.jackson.map.ObjectMapper mapper = new org.codehaus.jackson.map.ObjectMapper();
	    //There are other configuration options you can set.  This is the one I needed.
//	    mapper.configure(SerializationConfig.Feature.WRITE_ENUMS_USING_TO_STRING, true);

	    JsonSchema schema = mapper.generateJsonSchema(clazz);

	    return mapper.writerWithDefaultPrettyPrinter().writeValueAsString(schema);
	}
	
}
