#!/usr/bin/env python3
"""
Comprehensive Test Suite for Generational Improvement Framework

This test suite validates the functionality and robustness of the generational
iteration framework for the Klipper SDK.
"""

import os
import sys
import json
import tempfile
import shutil
import time
from datetime import datetime

# Add the klipper_sdk to the path
sys.path.insert(0, 'klipper_sdk/src')

from klipper_sdk.generational import GenerationTracker, GenerationalImprovementLoop, GenerationalBlueprintManager

def test_generation_tracker_basic_functionality():
    """Test basic GenerationTracker functionality."""
    print("🧪 Testing GenerationTracker Basic Functionality...")
    
    # Use temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        tracker = GenerationTracker(temp_dir)
        
        # Test 1: Register components
        result1 = tracker.register_component("test_component_1", 1, "Test Component 1")
        result2 = tracker.register_component("test_component_2", 2, "Test Component 2")
        
        assert result1 == True, "Failed to register first component"
        assert result2 == True, "Failed to register second component"
        
        # Test 2: Verify component registration
        gen1 = tracker.get_current_generation("test_component_1")
        gen2 = tracker.get_current_generation("test_component_2")
        
        assert gen1 == 1, f"Expected generation 1, got {gen1}"
        assert gen2 == 2, f"Expected generation 2, got {gen2}"
        
        # Test 3: Advance generation
        changes = {"improvements": ["test improvement"], "test": "data"}
        metrics = {"accuracy": 0.95, "speed": "fast"}
        
        result = tracker.advance_generation("test_component_1", changes, metrics)
        assert result == True, "Failed to advance generation"
        
        new_gen = tracker.get_current_generation("test_component_1")
        assert new_gen == 2, f"Expected generation 2 after advance, got {new_gen}"
        
        # Test 4: Verify generation history
        history = tracker.get_generation_history("test_component_1")
        assert history is not None, "No generation history found"
        assert len(history) == 1, f"Expected 1 generation in history, got {len(history)}"
        assert 1 in history, "Generation 1 not found in history"
        
        # Test 5: Verify metrics tracking
        metrics_trend = tracker.get_metrics_trend("test_component_1", "accuracy")
        assert len(metrics_trend) == 1, f"Expected 1 metrics record, got {len(metrics_trend)}"
        assert metrics_trend[0][1] == 0.95, f"Expected accuracy 0.95, got {metrics_trend[0][1]}"
        
        # Test 6: Generate report
        report = tracker.generate_report()
        assert "components" in report, "Report missing components section"
        assert "test_component_1" in report["components"], "Component not found in report"
        
        print("✅ GenerationTracker basic functionality tests passed!")

def test_generation_tracker_edge_cases():
    """Test GenerationTracker edge cases and error handling."""
    print("🧪 Testing GenerationTracker Edge Cases...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        tracker = GenerationTracker(temp_dir)
        
        # Test 1: Register duplicate component
        tracker.register_component("duplicate_test", 1, "Duplicate Component")
        result = tracker.register_component("duplicate_test", 1, "Duplicate Component")
        assert result == False, "Should not allow duplicate component registration"
        
        # Test 2: Get non-existent component
        gen = tracker.get_current_generation("non_existent_component")
        assert gen is None, "Should return None for non-existent component"
        
        info = tracker.get_component_info("non_existent_component")
        assert info is None, "Should return None for non-existent component info"
        
        # Test 3: Advance non-existent component
        result = tracker.advance_generation("non_existent", {"test": "data"})
        assert result == False, "Should not allow advancing non-existent component"
        
        # Test 4: Get metrics for non-existent component
        trend = tracker.get_metrics_trend("non_existent", "accuracy")
        assert len(trend) == 0, "Should return empty trend for non-existent component"
        
        print("✅ GenerationTracker edge case tests passed!")

def test_generation_tracker_persistence():
    """Test GenerationTracker data persistence."""
    print("🧪 Testing GenerationTracker Data Persistence...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create first tracker instance
        tracker1 = GenerationTracker(temp_dir)
        tracker1.register_component("persistent_test", 1, "Persistent Component")
        tracker1.advance_generation("persistent_test", {"change": "test"}, {"metric": 1.0})
        
        # Create second tracker instance with same directory
        tracker2 = GenerationTracker(temp_dir)
        
        # Verify data was persisted
        gen = tracker2.get_current_generation("persistent_test")
        assert gen == 2, f"Expected persisted generation 2, got {gen}"
        
        history = tracker2.get_generation_history("persistent_test")
        assert history is not None, "History should be persisted"
        assert len(history) == 1, "History length should be persisted"
        
        print("✅ GenerationTracker persistence tests passed!")

def test_generational_improvement_loop():
    """Test GenerationalImprovementLoop functionality."""
    print("🧪 Testing GenerationalImprovementLoop...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        tracker = GenerationTracker(temp_dir)
        improvement_loop = GenerationalImprovementLoop(tracker)
        
        # Register test component
        tracker.register_component("loop_test", 1, "Loop Test Component")
        
        # Define test functions
        def test_function():
            return {
                "metrics": {"performance": 0.8},
                "issues": ["needs optimization"]
            }
        
        def improvement_function(test_results):
            issues = test_results.get("issues", [])
            if "needs optimization" in issues:
                return ["Apply performance optimization"]
            return []
        
        def validation_function():
            return True  # Always pass for testing
        
        # Run improvement cycle
        result = improvement_loop.run_improvement_cycle(
            "loop_test",
            test_function,
            improvement_function,
            validation_function
        )
        
        assert result == True, "Improvement cycle should succeed"
        
        # Verify generation was advanced
        new_gen = tracker.get_current_generation("loop_test")
        assert new_gen == 2, f"Expected generation 2 after improvement, got {new_gen}"
        
        # Verify test results were stored
        assert "loop_test" in improvement_loop.test_results, "Test results should be stored"
        
        # Verify improvements were identified
        assert "loop_test" in improvement_loop.improvement_opportunities, "Improvements should be stored"
        assert len(improvement_loop.improvement_opportunities["loop_test"]) == 1, "Should identify 1 improvement"
        
        print("✅ GenerationalImprovementLoop tests passed!")

def test_batch_improvement():
    """Test batch improvement functionality."""
    print("🧪 Testing Batch Improvement...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        tracker = GenerationTracker(temp_dir)
        improvement_loop = GenerationalImprovementLoop(tracker)
        
        # Register multiple components
        components = ["batch_comp1", "batch_comp2", "batch_comp3"]
        for comp in components:
            tracker.register_component(comp, 1, f"Batch Component {comp}")
        
        # Define test functions for each component
        test_functions = {}
        improvement_functions = {}
        validation_functions = {}
        
        for comp in components:
            test_functions[comp] = lambda: {"metrics": {"quality": 0.7}, "issues": ["needs work"]}
            improvement_functions[comp] = lambda test_results: ["improve quality"] if test_results.get("issues") else []
            validation_functions[comp] = lambda: True
        
        # Run batch improvement
        results = improvement_loop.run_batch_improvement(
            components,
            test_functions,
            improvement_functions,
            validation_functions
        )
        
        # Verify all components were processed
        assert len(results) == 3, f"Expected 3 results, got {len(results)}"
        
        # Verify all improvements succeeded
        for comp, success in results.items():
            assert success == True, f"Improvement should succeed for {comp}"
            
            # Verify generation was advanced
            gen = tracker.get_current_generation(comp)
            assert gen == 2, f"Expected generation 2 for {comp}, got {gen}"
        
        print("✅ Batch improvement tests passed!")

def test_blueprint_manager():
    """Test GenerationalBlueprintManager functionality."""
    print("🧪 Testing GenerationalBlueprintManager...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        tracker = GenerationTracker(os.path.join(temp_dir, "tracker"))
        blueprint_manager = GenerationalBlueprintManager(tracker, os.path.join(temp_dir, "blueprints"))
        
        # Test 1: Register blueprint
        blueprint_content = """⫻kicklang:test
- name: test_blueprint
  description: Test Blueprint
  planes:
    structural:
      - name: test_phase
        steps:
          - name: test_step
            agent: test_agent
"""
        
        result = blueprint_manager.register_blueprint(
            "test_blueprint",
            blueprint_content,
            initial_generation=1,
            description="Test Blueprint for testing"
        )
        
        assert result is None, "Register blueprint should return None"
        
        # Test 2: Verify blueprint registration
        gen = tracker.get_current_generation("test_blueprint")
        assert gen == 1, f"Expected blueprint generation 1, got {gen}"
        
        # Test 3: Retrieve blueprint version
        retrieved_content = blueprint_manager.get_blueprint_version("test_blueprint", 1)
        assert retrieved_content is not None, "Should retrieve blueprint content"
        assert "test_blueprint" in retrieved_content, "Retrieved content should match original"
        
        # Test 4: Evolve blueprint
        new_blueprint_content = """⫻kicklang:test
- name: test_blueprint_v2
  description: Enhanced Test Blueprint
  planes:
    structural:
      - name: test_phase
        steps:
          - name: test_step
            agent: test_agent
          - name: new_step
            agent: new_agent
"""
        
        changes = {"improvements": ["Added new step and agent"]}
        metrics = {"complexity": 2.0}
        
        result = blueprint_manager.evolve_blueprint(
            "test_blueprint",
            new_blueprint_content,
            changes,
            metrics
        )
        
        assert result == True, "Blueprint evolution should succeed"
        
        # Test 5: Verify blueprint evolution
        new_gen = tracker.get_current_generation("test_blueprint")
        assert new_gen == 2, f"Expected blueprint generation 2, got {new_gen}"
        
        # Test 6: Compare generations
        comparison = blueprint_manager.compare_generations("test_blueprint", 1, 2)
        assert "blueprint" in comparison, "Comparison should contain blueprint name"
        assert comparison["generation_1"] == 1, "Comparison should show correct generations"
        assert comparison["generation_2"] == 2, "Comparison should show correct generations"
        
        # Test 7: Get latest blueprint
        latest = blueprint_manager.get_latest_blueprint("test_blueprint")
        assert latest is not None, "Should get latest blueprint"
        assert "new_step" in latest, "Latest should contain new content"
        
        print("✅ GenerationalBlueprintManager tests passed!")

def test_blueprint_file_management():
    """Test blueprint file management and versioning."""
    print("🧪 Testing Blueprint File Management...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        tracker = GenerationTracker(os.path.join(temp_dir, "tracker"))
        blueprint_manager = GenerationalBlueprintManager(tracker, os.path.join(temp_dir, "blueprints"))
        
        # Register a blueprint
        blueprint_content = "test content line 1\ntest content line 2"
        blueprint_manager.register_blueprint("file_test", blueprint_content, 1, "File test")
        
        # Verify files were created
        blueprint_dir = os.path.join(temp_dir, "blueprints", "file_test")
        assert os.path.exists(blueprint_dir), "Blueprint directory should be created"
        
        gen1_file = os.path.join(blueprint_dir, "gen_1.kl")
        assert os.path.exists(gen1_file), "Generation 1 file should be created"
        
        with open(gen1_file, 'r') as f:
            content = f.read()
            assert content == blueprint_content, "File content should match original"
        
        # Evolve blueprint and verify new file
        new_content = "test content line 1\ntest content line 2\ntest content line 3"
        blueprint_manager.evolve_blueprint("file_test", new_content, {"change": "added line"})
        
        gen2_file = os.path.join(blueprint_dir, "gen_2.kl")
        assert os.path.exists(gen2_file), "Generation 2 file should be created"
        
        with open(gen2_file, 'r') as f:
            content = f.read()
            assert content == new_content, "New file content should match evolved content"
        
        # Verify both versions still exist
        assert os.path.exists(gen1_file), "Original file should still exist"
        assert os.path.exists(gen2_file), "New file should exist"
        
        print("✅ Blueprint file management tests passed!")

def test_integration_scenario():
    """Test a complete integration scenario."""
    print("🧪 Testing Complete Integration Scenario...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Initialize all components
        tracker = GenerationTracker(os.path.join(temp_dir, "tracker"))
        improvement_loop = GenerationalImprovementLoop(tracker)
        blueprint_manager = GenerationalBlueprintManager(tracker, os.path.join(temp_dir, "blueprints"))
        
        # Scenario: Improve a content analysis system across generations
        
        # Generation 1: Basic system
        tracker.register_component("content_analyzer", 1, "Basic content analysis system")
        
        # Generation 1 blueprint
        gen1_blueprint = """⫻kicklang:content_analysis
- name: basic_analysis
  planes:
    agentic:
      - name: BasicAnalyzer
        role: Basic Content Analyzer
    structural:
      - name: analyze
        steps:
          - name: detect_type
            agent: BasicAnalyzer
"""
        
        blueprint_manager.register_blueprint("analysis_workflow", gen1_blueprint, 1, "Basic analysis workflow")
        
        # Simulate improvement cycle to Generation 2
        def test_gen1():
            return {
                "metrics": {"accuracy": 0.75, "coverage": 3},
                "issues": ["limited type support", "low accuracy"]
            }
        
        def identify_gen2_improvements(test_results):
            improvements = []
            if test_results["metrics"]["accuracy"] < 0.85:
                improvements.append("Enhance detection algorithms")
            if test_results["metrics"]["coverage"] < 5:
                improvements.append("Add support for more content types")
            return improvements
        
        def validate_gen2():
            return True
        
        improvement_loop.run_improvement_cycle(
            "content_analyzer",
            test_gen1,
            identify_gen2_improvements,
            validate_gen2
        )
        
        # Generation 2 blueprint
        gen2_blueprint = """⫻kicklang:content_analysis
- name: enhanced_analysis
  planes:
    agentic:
      - name: BasicAnalyzer
        role: Basic Content Analyzer
      - name: TypeValidator
        role: Type Validation Agent
    structural:
      - name: analyze
        steps:
          - name: detect_type
            agent: BasicAnalyzer
          - name: validate_type
            agent: TypeValidator
"""
        
        blueprint_manager.evolve_blueprint(
            "analysis_workflow",
            gen2_blueprint,
            {"improvements": ["Added validation step", "Enhanced type detection"]},
            {"accuracy": 0.88, "coverage": 5}
        )
        
        # Verify final state
        analyzer_gen = tracker.get_current_generation("content_analyzer")
        workflow_gen = tracker.get_current_generation("analysis_workflow")
        
        assert analyzer_gen == 2, f"Expected analyzer at generation 2, got {analyzer_gen}"
        assert workflow_gen == 2, f"Expected workflow at generation 2, got {workflow_gen}"
        
        # Verify we can retrieve both generations of blueprints
        gen1_content = blueprint_manager.get_blueprint_version("analysis_workflow", 1)
        gen2_content = blueprint_manager.get_blueprint_version("analysis_workflow", 2)
        
        assert gen1_content is not None, "Should retrieve generation 1 blueprint"
        assert gen2_content is not None, "Should retrieve generation 2 blueprint"
        assert "TypeValidator" not in gen1_content, "Generation 1 should not have validator"
        assert "TypeValidator" in gen2_content, "Generation 2 should have validator"
        
        print("✅ Complete integration scenario tests passed!")

def run_all_tests():
    """Run all tests and report results."""
    print("🧪 Running Comprehensive Generational Framework Test Suite")
    print("=" * 60)
    
    tests = [
        ("GenerationTracker Basic Functionality", test_generation_tracker_basic_functionality),
        ("GenerationTracker Edge Cases", test_generation_tracker_edge_cases),
        ("GenerationTracker Persistence", test_generation_tracker_persistence),
        ("GenerationalImprovementLoop", test_generational_improvement_loop),
        ("Batch Improvement", test_batch_improvement),
        ("GenerationalBlueprintManager", test_blueprint_manager),
        ("Blueprint File Management", test_blueprint_file_management),
        ("Complete Integration Scenario", test_integration_scenario),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_function in tests:
        try:
            print(f"\n📋 Running: {test_name}")
            test_function()
            passed += 1
            print(f"✅ {test_name}: PASSED")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name}: FAILED with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Generational framework is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please review the implementation.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)