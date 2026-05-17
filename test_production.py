#!/usr/bin/env python3
"""
Test script to verify production readiness
"""

import sys
from modules.logger import setup_logger
from main import create_reel, create_batch

logger = setup_logger('test')

def test_single_reel():
    """Test creating a single reel"""
    logger.info("=" * 60)
    logger.info("TEST 1: Single Reel Creation")
    logger.info("=" * 60)
    
    try:
        result = create_reel()
        if result:
            logger.info("✓ TEST PASSED: Single reel created successfully")
            return True
        else:
            logger.error("✗ TEST FAILED: Single reel creation returned None")
            return False
    except Exception as e:
        logger.error(f"✗ TEST FAILED: {e}", exc_info=True)
        return False

def test_batch_small():
    """Test creating a small batch"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 2: Small Batch (3 reels)")
    logger.info("=" * 60)
    
    try:
        results, failed = create_batch(3, parallel=False)
        
        if len(results) >= 2:  # At least 2 out of 3 should succeed
            logger.info(f"✓ TEST PASSED: Created {len(results)}/3 reels")
            return True
        else:
            logger.error(f"✗ TEST FAILED: Only {len(results)}/3 reels created")
            return False
    except Exception as e:
        logger.error(f"✗ TEST FAILED: {e}", exc_info=True)
        return False

def test_retry_mechanism():
    """Test retry mechanism"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 3: Retry Mechanism")
    logger.info("=" * 60)
    
    from modules.retry_handler import retry_with_backoff
    
    attempt_count = [0]
    
    @retry_with_backoff(max_retries=3, initial_delay=0.1, exceptions=(ValueError,))
    def failing_function():
        attempt_count[0] += 1
        if attempt_count[0] < 3:
            raise ValueError(f"Attempt {attempt_count[0]} failed")
        return "Success"
    
    try:
        result = failing_function()
        if result == "Success" and attempt_count[0] == 3:
            logger.info("✓ TEST PASSED: Retry mechanism works correctly")
            return True
        else:
            logger.error("✗ TEST FAILED: Retry mechanism didn't work as expected")
            return False
    except Exception as e:
        logger.error(f"✗ TEST FAILED: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("🧪 Starting Production Readiness Tests")
    logger.info("=" * 60)
    
    tests = [
        ("Single Reel Creation", test_single_reel),
        ("Small Batch Processing", test_batch_small),
        ("Retry Mechanism", test_retry_mechanism)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            logger.error(f"Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        logger.info(f"{status} - {test_name}")
    
    logger.info("=" * 60)
    logger.info(f"Results: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        logger.info("🎉 ALL TESTS PASSED - System is production ready!")
        return 0
    else:
        logger.error("⚠ SOME TESTS FAILED - Review logs before production use")
        return 1

if __name__ == "__main__":
    sys.exit(main())
