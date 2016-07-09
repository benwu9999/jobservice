package com.wungong.jobservice.model;

import lombok.Data;

public class Address {
	
	final private State state;
	final private Country country;
	final private String aptNumber;
	final private String streeAddress;
	final private String city;
	final private Integer zipCode;
	
	public Address(State state, Country country, String aptNumber, String streeAddress, String city, Integer zipCode) {
		this.state = state;
		this.country = country;
		this.aptNumber = aptNumber;
		this.streeAddress = streeAddress;
		this.city = city;
		this.zipCode = zipCode;
	}

	public State getState() {
		return state;
	}

	public Country getCountry() {
		return country;
	}

	public String getAptNumber() {
		return aptNumber;
	}

	public String getStreeAddress() {
		return streeAddress;
	}

	public String getCity() {
		return city;
	}

	public Integer getZipCode() {
		return zipCode;
	}

}
