package com.wungong.jobservice;

import java.util.UUID;

import com.wungong.jobservice.model.Job;

public class CassandraSpike {
	
	public static void main(String[] args) throws Exception {
		
		Job job = new Job(UUID.randomUUID());
		new CassandraConfig().cassandraTemplate().insert(job);
	}

}
