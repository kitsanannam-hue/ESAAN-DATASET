
#!/usr/bin/env python3
"""
Data Quality Checker
====================
ตรวจสอบคุณภาพข้อมูล Thai-Jazz ML Dataset
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any
import re


class DataQualityChecker:
    """ตรวจสอบคุณภาพข้อมูล"""
    
    def __init__(self, data_dir: str = "output"):
        self.data_dir = Path(data_dir)
        self.issues = []
        self.stats = {}
    
    def check_music_notation(self) -> Dict[str, Any]:
        """ตรวจสอบคุณภาพข้อมูล Musical Notation"""
        notation_path = self.data_dir / "music_notation_dataset" / "musical_notation.json"
        
        if not notation_path.exists():
            self.issues.append("❌ ไม่พบไฟล์ musical_notation.json")
            return {}
        
        with open(notation_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        df = pd.DataFrame(data)
        
        quality_report = {
            'total_records': len(df),
            'missing_values': df.isnull().sum().to_dict(),
            'duplicate_records': df.duplicated().sum(),
            'type_distribution': df['type'].value_counts().to_dict() if 'type' in df.columns else {},
            'page_coverage': {
                'min_page': int(df['page'].min()) if 'page' in df.columns else 0,
                'max_page': int(df['page'].max()) if 'page' in df.columns else 0,
                'unique_pages': int(df['page'].nunique()) if 'page' in df.columns else 0
            }
        }
        
        # ตรวจสอบข้อมูลที่ไม่สมบูรณ์
        if quality_report['missing_values'].get('notation', 0) > 0:
            self.issues.append(f"⚠️  พบ notation ที่หายไป {quality_report['missing_values']['notation']} รายการ")
        
        if quality_report['duplicate_records'] > 0:
            self.issues.append(f"⚠️  พบข้อมูลซ้ำ {quality_report['duplicate_records']} รายการ")
        
        return quality_report
    
    def check_phin_dataset(self) -> Dict[str, Any]:
        """ตรวจสอบคุณภาพข้อมูล Phin Dataset"""
        phin_path = self.data_dir / "phin_dataset" / "phin_dataset_complete.json"
        
        if not phin_path.exists():
            self.issues.append("❌ ไม่พบไฟล์ phin_dataset_complete.json")
            return {}
        
        with open(phin_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        quality_report = {
            'tuning_systems': len(data.get('tuning_systems', [])),
            'lai_patterns': len(data.get('lai_patterns', [])),
            'techniques': len(data.get('techniques', [])),
            'artists': len(data.get('artists', []))
        }
        
        # ตรวจสอบความสมบูรณ์
        for key, count in quality_report.items():
            if count == 0:
                self.issues.append(f"⚠️  ไม่พบข้อมูล {key}")
        
        return quality_report
    
    def check_ml_dataset(self) -> Dict[str, Any]:
        """ตรวจสอบคุณภาพข้อมูล ML Dataset"""
        ml_path = self.data_dir / "ml_dataset" / "complete_ml_dataset.json"
        
        if not ml_path.exists():
            self.issues.append("❌ ไม่พบไฟล์ complete_ml_dataset.json")
            return {}
        
        with open(ml_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        quality_report = {
            'thai_features': len(data.get('thai_traditional_features', {})),
            'jazz_features': len(data.get('jazz_modern_features', {})),
            'hybridization_techniques': len(data.get('hybridization_techniques', [])),
            'scale_mappings': len(data.get('thai_jazz_scale_mappings', []))
        }
        
        return quality_report
    
    def clean_duplicates(self):
        """ลบข้อมูลซ้ำ"""
        notation_path = self.data_dir / "music_notation_dataset" / "musical_notation.csv"
        
        if notation_path.exists():
            df = pd.read_csv(notation_path)
            original_count = len(df)
            df_clean = df.drop_duplicates()
            cleaned_count = len(df_clean)
            
            if original_count > cleaned_count:
                df_clean.to_csv(notation_path, index=False)
                df_clean.to_json(
                    self.data_dir / "music_notation_dataset" / "musical_notation.json",
                    orient='records', force_ascii=False, indent=2
                )
                print(f"✅ ลบข้อมูลซ้ำ {original_count - cleaned_count} รายการ")
    
    def validate_thai_terms(self) -> List[str]:
        """ตรวจสอบคำศัพท์ภาษาไทย"""
        issues = []
        
        # ตรวจสอบ Phin lai patterns
        lai_path = self.data_dir / "phin_dataset" / "phin_lai_patterns.json"
        if lai_path.exists():
            with open(lai_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for item in data:
                if not item.get('name_thai'):
                    issues.append(f"⚠️  ไม่มีชื่อภาษาไทยสำหรับ {item.get('name_english', 'unknown')}")
        
        return issues
    
    def generate_report(self) -> str:
        """สร้างรายงานคุณภาพข้อมูล"""
        print("=" * 70)
        print("รายงานคุณภาพข้อมูล Thai-Jazz ML Dataset")
        print("=" * 70)
        
        # ตรวจสอบ Musical Notation
        print("\n📝 Musical Notation Dataset:")
        notation_quality = self.check_music_notation()
        if notation_quality:
            print(f"  รวมทั้งหมด: {notation_quality['total_records']} รายการ")
            print(f"  หน้าที่มีข้อมูล: {notation_quality['page_coverage']['unique_pages']} หน้า")
            print(f"  ข้อมูลซ้ำ: {notation_quality['duplicate_records']} รายการ")
        
        # ตรวจสอบ Phin Dataset
        print("\n🎵 Phin Dataset:")
        phin_quality = self.check_phin_dataset()
        if phin_quality:
            print(f"  ระบบการปรับเสียง: {phin_quality['tuning_systems']}")
            print(f"  ลายเพลง (Lai): {phin_quality['lai_patterns']}")
            print(f"  เทคนิค: {phin_quality['techniques']}")
            print(f"  ศิลปิน: {phin_quality['artists']}")
        
        # ตรวจสอบ ML Dataset
        print("\n🤖 ML Dataset:")
        ml_quality = self.check_ml_dataset()
        if ml_quality:
            print(f"  Thai Features: {ml_quality['thai_features']}")
            print(f"  Jazz Features: {ml_quality['jazz_features']}")
            print(f"  Hybridization: {ml_quality['hybridization_techniques']}")
            print(f"  Scale Mappings: {ml_quality['scale_mappings']}")
        
        # แสดงปัญหาที่พบ
        if self.issues:
            print("\n⚠️  ปัญหาที่พบ:")
            for issue in self.issues:
                print(f"  {issue}")
        else:
            print("\n✅ ไม่พบปัญหาคุณภาพข้อมูล")
        
        # ตรวจสอบคำศัพท์ภาษาไทย
        thai_issues = self.validate_thai_terms()
        if thai_issues:
            print("\n📚 คำศัพท์ภาษาไทย:")
            for issue in thai_issues:
                print(f"  {issue}")
        
        print("\n" + "=" * 70)
        
        return "Quality check complete"


def main():
    """Run quality check"""
    checker = DataQualityChecker()
    
    # สร้างรายงาน
    checker.generate_report()
    
    # ทำความสะอาดข้อมูล
    print("\n🧹 กำลังทำความสะอาดข้อมูล...")
    checker.clean_duplicates()
    
    print("\n✨ เสร็จสิ้น!")


if __name__ == "__main__":
    main()
