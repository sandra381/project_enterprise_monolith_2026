/*
 * Copyright 2012-2025 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.springframework.samples.petclinic.owner;

import java.util.Optional;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface OwnerRepository extends JpaRepository<Owner, Integer> {

	/**
	 * Delivery 5 - FinOps: EntityGraph carga owners + pets + visits + type en una sola
	 * consulta, eliminando completamente el problema N+1.
	 */
	@EntityGraph(attributePaths = { "pets", "pets.visits", "pets.type" })
	@Query("SELECT DISTINCT owner FROM Owner owner WHERE owner.lastName LIKE :lastName%")
	Page<Owner> findByLastNameStartingWith(@Param("lastName") String lastName, Pageable pageable);

	Optional<Owner> findById(Integer id);

}