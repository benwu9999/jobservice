package com.wungong.jobservice.model;

import lombok.Data;

@Data
public class Address {
	
	final private State state;
	final private Country country;
	final private String aptNumber;
	final private String streeAddress;
	final private String city;
	final private Integer zipCode;

}
