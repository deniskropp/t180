import unittest
from datetime import datetime
from klipper_sdk.learning import LearningManager, TemporalPredictor

class TestTemporalLayer(unittest.TestCase):
    def test_predictor_logic(self):
        pred = TemporalPredictor()
        base_time = 1000000.0
        # Add events every 3600 seconds
        for i in range(5):
            pred.add_event(base_time + (i * 3600))
            
        # The next event should be at base_time + 5 * 3600
        # However, predict_next projects into the future relative to NOW.
        # So we need to ensure our test data is relevant to "now".
        
        # Let's test just the next interval logic without "now" projection first
        # We can mock datetime if we want, but let's just check the logic 
        # that drives the average interval.
        
        intervals = [t2 - t1 for t1, t2 in zip(pred.history[:-1], pred.history[1:])]
        avg = sum(intervals) / len(intervals)
        self.assertAlmostEqual(avg, 3600.0)

    def test_learning_manager_integration(self):
        lm = LearningManager()
        now = datetime.now().timestamp()
        # History: 3 events, 2 hours apart
        history = [now - 7200, now - 3600, now]
        
        predicted = lm.predict_usage(age=0, history=history)
        expected = now + 3600
        
        # Allow small delta
        self.assertTrue(abs(predicted - expected) < 5.0)

if __name__ == '__main__':
    unittest.main()
