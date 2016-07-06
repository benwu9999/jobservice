package com.wungong.jobservice.model;

import lombok.Data;

@Data
public class Employer {
	
	private final EmployerId employerId;
	
	private final String employerName;
	
	private Address employerAddress;

}
