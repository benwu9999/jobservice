package com.wungong.jobservice;

import java.util.UUID;

import com.datastax.driver.core.Cluster;
import com.datastax.driver.core.policies.DefaultRetryPolicy;
import com.datastax.driver.extras.codecs.enums.EnumNameCodec;
import com.datastax.driver.mapping.Mapper;
import com.datastax.driver.mapping.MappingManager;
import com.wungong.jobservice.model.Job;
import com.wungong.jobservice.model.JobType;
import com.wungong.jobservice.model.State;

public class CassandraSpike {
	
	public static void main(String[] args) throws Exception {
		
		Job job = new Job(UUID.randomUUID());
		Cluster cluster = Cluster
				.builder()
				.addContactPoint("localhost")
				.withRetryPolicy(DefaultRetryPolicy.INSTANCE)
				.build();
		EnumNameCodec<JobType> myEnumCodec1 = new EnumNameCodec<JobType>(JobType.class);
		EnumNameCodec<State> myEnumCodec2 = new EnumNameCodec<State>(State.class);
		cluster.getConfiguration().getCodecRegistry().register(myEnumCodec1);
		cluster.getConfiguration().getCodecRegistry().register(myEnumCodec2);
		MappingManager mappingManager = new MappingManager(cluster.connect("jobservice"));
		Mapper<Job> mapper = mappingManager.mapper(Job.class);
		mapper.save(job);
	}

}
