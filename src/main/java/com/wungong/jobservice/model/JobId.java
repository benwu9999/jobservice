package com.wungong.jobservice.model;

import java.util.UUID;

public class JobId {

	final private UUID id;

	public JobId(UUID id) {
		this.id = id;
	}
	
	public JobId(String id) {
		this.id = UUID.fromString(id);
	}
	
	public UUID id(){
		return id;
	}

}
