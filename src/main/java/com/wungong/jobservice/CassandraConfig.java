package com.wungong.jobservice;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.core.env.Environment;

import com.datastax.driver.core.Cluster;
import com.datastax.driver.core.CodecRegistry;
import com.datastax.driver.core.Session;
import com.datastax.driver.core.policies.DefaultRetryPolicy;
import com.datastax.driver.extras.codecs.enums.EnumNameCodec;
import com.datastax.driver.mapping.MappingManager;
import com.wungong.jobservice.model.JobType;
import com.wungong.jobservice.model.State;

@Configuration
@PropertySource(value = { "classpath:cassandra.properties" })
public class CassandraConfig {

  	@Autowired
  	private Environment env;

	@Bean
	public MappingManager mappingManager() throws Exception {
		return new MappingManager(session());
	}

	private Session session() {
		Cluster cluster = Cluster
				.builder()
				.addContactPoint(env.getProperty("jobservice.cassandra.contactpoints"))
				.withRetryPolicy(DefaultRetryPolicy.INSTANCE)
				.build();
		CodecRegistry registry = cluster.getConfiguration().getCodecRegistry();
		registry.register(new EnumNameCodec<JobType>(JobType.class));
		registry.register(new EnumNameCodec<State>(State.class));
		return cluster.connect(env.getProperty("jobservice.cassandra.keyspace"));
	}
}
