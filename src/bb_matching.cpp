/*
 * Launching bb_matching algorithm many times on random generated data 
 */

#include <stdio.h>
#include "geometry_utils.h"
#include <ctime>
#include <chrono>
#include <iostream>
#include <fstream>

int W = 620;
int H = 480;

using namespace cv;

eod::ExtendedObjectInfo generate_rect(){
    int x1 = std::rand() % W;
    int x2 = std::rand() % W;
    int y1 = std::rand() % H;
    int y2 = std::rand() % H;
    
    int x = min(x1,x2);
    int y = min(y1,y2);
    
    int h = max(x1,x2) - x;
    int w = max(y1,y2) - y;
    
    return eod::ExtendedObjectInfo(x,y,w,h);
    
}

void generate_rects(int N, std::vector <eod::ExtendedObjectInfo> &rects){
    rects.clear();
    for( int i = 0 ; i < N ; i++){
        rects.push_back(generate_rect());
    }    
}

int main(int argc, char **argv){
    if( argc < 5){
        printf("Wrong usage!\nUsage: ./bb_matching min_rects max_rects n_tries path_to_results\nExample: ./bb_matching 10 100 5 ../../data/bb_matching_10_100.csv\n");
        return -1;
    }    
    int min_rects = std::atoi(argv[1]);
    int max_rects = std::atoi(argv[2]);    
    int n_tries = std::atoi(argv[3]);
    int iou_threshold_d = 0.75;
    
    std::ofstream results_file;
    //std::string = argv[4]
    results_file.open (argv[4]);
    
    results_file << "RectsA,RectsB";
    for(int n = 0 ; n < n_tries ; n++)
        results_file << ",time" <<n;
    results_file<<"\n";
    
    printf("Calculation started\n");
    
    std::srand(std::time(nullptr));
    
    std::vector<eod::ExtendedObjectInfo> rectsA;
    std::vector<eod::ExtendedObjectInfo> rectsB;
    for( int i = min_rects ; i < max_rects ; i++){
        for( int j = min_rects ; j < max_rects ; j++){
            results_file<<i<<","<<j;
            for( int n = 0 ; n < n_tries ; n++){
                generate_rects(i, rectsA);
                generate_rects(j, rectsB);
                
                std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();            
                Mat_<double> closenessMapD = createClosenessMap(&rectsA, &rectsB, iou_threshold_d);
                Mat mask(closenessMapD.size(), CV_8UC1, Scalar(255,255,255));            
                
                while( true ){
                    double min, max = 0;
                    Point min_loc, max_loc;
                    minMaxLoc(closenessMapD, &min, &max, &min_loc, &max_loc, mask);
                    if( max == 0 ) break;                               
                        
                    eod::ExtendedObjectInfo newone;                
                    newone = rectsA[max_loc.y] & rectsB[max_loc.x];   
                                    
                    mask.row(max_loc.y).setTo(Scalar(0,0,0));                                    
                    mask.col(max_loc.x).setTo(Scalar(0,0,0));                                
                }
                mask.release();
                closenessMapD.release();
                std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
                double elapsed_time = std::chrono::duration_cast<std::chrono::milliseconds>(end-begin).count();
                printf("[%i, %i]: %f ms\n",i,j,elapsed_time);
                results_file<<","<<elapsed_time;
            }
            results_file<<"\n";
        }
    }
    results_file.close();
    printf("File %s saved\n",argv[4]);
    return 0;
    
}
