package com.wungong.jobservice.model;

import java.util.UUID;

public class EmployerId {
	
	final private UUID id;

	public EmployerId(UUID id) {
		this.id = id;
	}
	
	public EmployerId(String id) {
		this.id = UUID.fromString(id);
	}
	
	public UUID id(){
		return id;
	}
	
	public String toString() {
		return id.toString();
	}

}
