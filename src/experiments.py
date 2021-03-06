from mfcc import mfcc
from features import files_to_features, unfold_matrix_list_with_labels, knn_train_features
from gmm import train_gmm_set, test_gmms
from knn import train_knn, test_knn
import numpy as np
import utilities

def experiment1(n_neighbors=5):
    """
    Train a knn model on ~1000 white noise and ~1000 voice snippets.
    Test with ~20 held out white noise and voice snippets.
    """
    voice_features, _ = files_to_features('data/an4/wav/an4_clstk')
    voice_labels = ["voice"] * voice_features.shape[0]

    white_noise_features, _ = files_to_features('data/white_noise/train')
    white_noise_labels = ["white_noise"] * white_noise_features.shape[0]

    print "Features computed, beginning training...."

    all_features = np.vstack((white_noise_features, voice_features))
    all_labels = np.concatenate((white_noise_labels, voice_labels))
    clf = train_knn(all_features, all_labels, n_neighbors)

    print "Training completed, testing..."

    white_noise_tests, _ = files_to_features('data/white_noise/test')
    voice_tests, _ = files_to_features('data/an4/wav/an4test_clstk')

    print "White noise test:", test_knn(clf, white_noise_tests)
    print "Voice test:", test_knn(clf, voice_tests)

def experiment2(n_neighbors=3):
    """
    Train a knn with 12 voice samples from each of 6 people (3 male, 3 female), and 12 samples of white noise.
    Test with 1 voice sample from each of the 6, and 1 sample of white noise.
    """
    train_data, train_labels = files_to_features('data/an4_pairwise/train_full')
    new_train_data, new_train_labels = unfold_matrix_list_with_labels(train_data, train_labels)

    clf = train_knn(new_train_data, new_train_labels, n_neighbors)

    test_data, exp_labels = files_to_features('data/an4_pairwise/test_full')

    print [(test, exp, test == exp) for test, exp in zip(test_knn(clf, test_data, list(set(exp_labels))), exp_labels)]

def experiment3(n_neighbors=3):
    """
    Train a knn with 12 voice samples from each of 2 people (1 male, 1 female), and 12 samples of white noise.
    Test with 1 voice sample from each of the people, and 1 sample of white noise.
    """

    train_data, train_labels = files_to_features('data/an4_pairwise/train')
    clf = train_knn(train_data, train_labels, n_neighbors)

    test_data, exp_labels = files_to_features('data/an4_pairwise/test')

    print [(test, exp, test == exp) for test, exp in zip(test_knn(clf, test_data), exp_labels)]

def experiment4(n_neighbors=3):
    """
    Train a knn with 7 voice samples from each of Nathan and Sasha
    Test with two voice samples from each of us.
    """

    train_data, train_labels = files_to_features('data/natasha_pairwise/train')
    clf = train_knn(train_data, train_labels, n_neighbors)

    test_data, exp_labels = files_to_features('data/natasha_pairwise/test')

    print [(test, exp, test == exp) for test, exp in zip(test_knn(clf, test_data), exp_labels)]

def experiment5(n_neighbors=3):
    """
    Train a knn with 7 voice samples from each of Nathan, Sasha, and Pardo
    Test with two voice samples from each of us
    """
    train_data, train_labels = files_to_features('data/natasha_and_pardo/train')
    new_train_data, new_train_labels = unfold_matrix_list_with_labels(train_data, train_labels)
    clf = train_knn(new_train_data, new_train_labels, n_neighbors)
    utilities.save(clf, 'nathan_sasha_pardo_knn_clf.p')

    test_data, exp_labels = files_to_features('data/natasha_and_pardo/test')

    print [(test, exp, test == exp) for test, exp in zip(test_knn(clf, test_data, list(set(exp_labels))), exp_labels)]

def experiment6():
    """
    Train a gmm with 7 voice samples from each of Nathan, Sasha, and Pardo
    Test with two voice samples from each of us
    """
    train_data, train_labels = files_to_features('data/natasha_and_pardo/train')
    unique_train_labels = set(train_labels)
    gmm_train_data = {label: [] for label in unique_train_labels}
    
    new_train_data, new_train_labels = unfold_matrix_list_with_labels(train_data, train_labels)

    for feature_vector, label in zip(new_train_data, new_train_labels):
        gmm_train_data[label].append(feature_vector)

    gmm_dict = train_gmm_set(gmm_train_data)
    utilities.save(gmm_dict, 'nathan_sasha_pardo_gmm_dict.p')
    
    test_data, exp_labels = files_to_features('data/natasha_and_pardo/test')
    
    print [(test, exp, test == exp) for test, exp in zip(test_gmms(gmm_dict, test_data), exp_labels)]

def experiment7():
    """ Train a gmm with 12 voice samples from each of 6 people (3 male, 3 female), and 12 samples of white noise. 
        Test with 1 voice sample from each of the 6, and 1 sample of white noise. """
    train_data, train_labels = files_to_features('data/an4_pairwise/train_full')
    unique_train_labels = set(train_labels)
    gmm_train_data = {label: [] for label in unique_train_labels}
    new_train_data, new_train_labels = unfold_matrix_list_with_labels(train_data, train_labels)

    for feature_vector, label in zip(new_train_data, new_train_labels):
        gmm_train_data[label].append(feature_vector)

    gmm_dict = train_gmm_set(gmm_train_data)
    
    test_data, exp_labels = files_to_features('data/an4_pairwise/test_full')
    
    print [(test, exp, test == exp) for test, exp in zip(test_gmms(gmm_dict, test_data), exp_labels)]

def experiment8():
    """Train a gmm with ~12 voice samples from each of 19 people and 1 set of white noise.

    Test with 1-2 voice samples from each class."""
    train_data, train_labels = files_to_features('data/lots_of_people/train')
    unique_train_labels = set(train_labels)
    gmm_train_data = {label: [] for label in unique_train_labels}
    new_train_data, new_train_labels = unfold_matrix_list_with_labels(train_data, train_labels)

    for feature_vector, label in zip(new_train_data, new_train_labels):
        gmm_train_data[label].append(feature_vector)

    gmm_dict = train_gmm_set(gmm_train_data)
    
    test_data, exp_labels = files_to_features('data/lots_of_people/test')
    
    results = [(test, exp, test == exp) for test, exp in zip(test_gmms(gmm_dict, test_data), exp_labels)]
    print results
    print

    for res in results:
        if res[2]:
            print "Matched %s to %s -- correct" % (res[1], res[0])
        else:
            print "Expected %s, got %s -- incorrect" % (res[1], res[0])

    n_correct = len([r for r in results if r[2]])
    n_total = len(results)
    n_incorrect = n_total - n_correct
    print "%d/%d correct (%0.2f)" % (n_correct, n_total, float(n_correct)/n_total)
    print "%d/%d incorrect (%0.2f)" % (n_incorrect, n_total, float(n_incorrect)/n_total)

def experiment9():
    """Train a gmm with a bunch of samples from ~20 CS professors and Sara's kid.

    Test with 1-2 voice samples from each class."""
    gmm_dict = utilities.load('professor_gmms_train.p')
    
    test_data, exp_labels = files_to_features('data/professors_split/train')
    
    preds, probs = test_gmms(gmm_dict, test_data)
    results = [(test, exp, test == exp) for test, exp in zip(preds, exp_labels)]

    for res in results:
        if res[2]:
            print "Matched %s to %s -- correct" % (res[1], res[0])
        else:
            print "Expected %s, got %s -- incorrect" % (res[1], res[0])

    n_correct = len([r for r in results if r[2]])
    n_total = len(results)
    n_incorrect = n_total - n_correct
    print "%d/%d correct (%0.2f)" % (n_correct, n_total, float(n_correct)/n_total)
    print "%d/%d incorrect (%0.2f)" % (n_incorrect, n_total, float(n_incorrect)/n_total)

def experiment10():
    """Check a bunch of local recordings of myself in different rooms against the professors,
    and see if they're consistent.

    Parsing out if trouble is matching different recording scenarios vs jumbled on server."""

    gmm_dict = utilities.load('professor_gmms.p')

    test_data, locations = files_to_features('data/sasha_rooms')
    preds, probs = test_gmms(gmm_dict, test_data)
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Sasha (top prediction and top six in prediction order):\n"
    for i in range(len(locations)):
        print "Top prediction:", probs[i][-1][0]
        print "Top six:", [name for name, _ in reversed(probs[i][-6:])]
        print

    test_data, locations = files_to_features('data/nathan_rooms')
    preds, probs = test_gmms(gmm_dict, test_data)
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Nathan (top prediction and top six in prediction order):\n"
    for i in range(len(locations)):
        print "Top prediction:", probs[i][-1][0]
        print "Top six:", [name for name, _ in reversed(probs[i][-6:])]
        print

def experiment11():
    """Check a bunch of downloaded website recordings of myself in the same room
    against the professors, and see if they're consistent.

    Same goal as experiment 10."""

    gmm_dict = utilities.load('professor_gmms.p')

    test_data, labels = files_to_features('data/sasha_website')

    preds, probs = test_gmms(gmm_dict, test_data)

    for i in range(len(probs)):
        print labels[i], probs[i]
        print

def experiment12():
    """Train a knn with a bunch of samples from ~20 CS professors and Sara's kid.

    Test with 1 voice samples from each class."""
    train_data, train_labels = utilities.load('professor_knn_features_train.p')

    clf = train_knn(train_data, train_labels, n_neighbors=5)
    
    test_data, exp_labels = files_to_features('data/professors_split/test')
    
    preds = test_knn(clf, test_data)
    results = [(test, exp, test == exp) for exp, test in zip(preds, exp_labels)]

    for res in results:
        if res[2]:
            print "Matched %s to %s -- correct" % (res[1], res[0])
        else:
            print "Expected %s, got %s -- incorrect" % (res[1], res[0])

    n_correct = len([r for r in results if r[2]])
    n_total = len(results)
    n_incorrect = n_total - n_correct
    print "%d/%d correct (%0.2f)" % (n_correct, n_total, float(n_correct)/n_total)
    print "%d/%d incorrect (%0.2f)" % (n_incorrect, n_total, float(n_incorrect)/n_total)

def experiment13():
    """Check a bunch of local recordings of myself in different rooms against the professors,
    and see if they're consistent, using KNNs.

    Parsing out if trouble is matching different recording scenarios vs jumbled on server."""
    train_data, train_labels = utilities.load('professor_knn_features.p')

    clf = train_knn(train_data, train_labels, n_neighbors=5)

    test_data, locations = files_to_features('data/sasha_rooms')

    preds = test_knn(clf, test_data)
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Sasha (top predictions):\n"
    for i in range(len(locations)):
        print "Top prediction:", preds[i]
        print

    test_data, locations = files_to_features('data/nathan_rooms')

    preds = test_knn(clf, test_data)
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Nathan (top predictions):\n"
    for i in range(len(locations)):
        print "Top prediction:", preds[i]
        print

def experiment14():
    """Test Fatemah and Goce's non-English recordings against the trained English GMMs.

    Expecting to see their voices matched to themselves."""

    gmm_dict = utilities.load('professor_gmms.p')

    test_data, exp_labels = files_to_features('data/multi_lingual')
    
    preds, probs = test_gmms(gmm_dict, test_data)
    results = [(test, exp, test == exp) for test, exp in zip(preds, exp_labels)]

    for res in results:
        if res[2]:
            print "Matched %s to %s -- correct" % (res[1], res[0])
        else:
            print "Expected %s, got %s -- incorrect" % (res[1], res[0])

    n_correct = len([r for r in results if r[2]])
    n_total = len(results)
    n_incorrect = n_total - n_correct
    print "%d/%d correct (%0.2f)" % (n_correct, n_total, float(n_correct)/n_total)
    print "%d/%d incorrect (%0.2f)" % (n_incorrect, n_total, float(n_incorrect)/n_total)

def experiment15():
    """Test Fatemah and Goce's non-English recordings against the trained English KNNs.

    Expecting to see their voices matched to themselves."""
    train_data, train_labels = utilities.load('professor_knn_features.p')

    clf = train_knn(train_data, train_labels, n_neighbors=5)
    
    test_data, exp_labels = files_to_features('data/multi_lingual')
    
    preds = test_knn(clf, test_data)
    results = [(test, exp, test == exp) for exp, test in zip(preds, exp_labels)]

    for res in results:
        if res[2]:
            print "Matched %s to %s -- correct" % (res[1], res[0])
        else:
            print "Expected %s, got %s -- incorrect" % (res[1], res[0])

    n_correct = len([r for r in results if r[2]])
    n_total = len(results)
    n_incorrect = n_total - n_correct
    print "%d/%d correct (%0.2f)" % (n_correct, n_total, float(n_correct)/n_total)
    print "%d/%d incorrect (%0.2f)" % (n_incorrect, n_total, float(n_incorrect)/n_total)
