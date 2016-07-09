package com.wungong.jobservice.persistence;

import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.cassandra.core.CassandraOperations;
import org.springframework.stereotype.Component;

import com.datastax.driver.core.Cluster;
import com.datastax.driver.core.Session;
import com.wungong.jobservice.model.Job;
import com.wungong.jobservice.utils.Settings;

@Component
public class JobRepositoryImpl implements JobRepository{
	
	@Autowired
	Settings settings;
	
	@Autowired
	CassandraOperations cassandraTemplate;

	@Override
	public UUID jobId() {
		// TODO Auto-generated method stub
		return UUID.randomUUID();
	}

	@Override
	public Job jobOfId(UUID jobId) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Boolean remove(Job jobToDelete) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void add(Job convertToJob) {
	}
	
}
